from sqlalchemy.orm import Session
from app.access_mapping import repository
from app.ingestion import repository as ingestion_repository
from app.access_mapping.schemas import FileRiskDetailsResponse, PaginatedFileRiskDetailsResponse, conf, SendViolationsEmailRequest
import app.scanning.service as scanning_service
from operator import attrgetter
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from app.authentication.models import User
from app.roles.repository import get_category_by_subcategory_name
from app.authentication.service import test_route


# Method for getting all employees with access to a file
def get_file_employees_with_access(db: Session, file_id: int):
    fetched_employees_records = repository.get_file_employees_with_access(db=db, file_id=file_id)
    has_been_scanned = scanning_service.check_file_has_scan(db=db, file_id=file_id)
    latest_scan_results = scanning_service.get_file_latest_scan_results(db=db, file_id=file_id)

    return get_file_employees_with_access_from_data(
        db=db,
        fetched_employees_records=fetched_employees_records,
        has_been_scanned=has_been_scanned,
        latest_scan_results=latest_scan_results
    )

# Method for returning all files and their access for each employee in a list
def get_employee_violated_files(db: Session, employees: list):
    for employee in employees:
        files = []

        user_id = employee["user"].user_id

        # Get employee file IDs that they have access to
        user_files = ingestion_repository.get_user_files(db, employee["user"].user_id)
        
        # Run a detection on each file
        for file in user_files:
            result = get_file_employees_with_access(db, file["file"].ingestion_file_id)

            matched_user = next((u for u in result if u["user_id"] == user_id), None)

            if matched_user:
                f = {
                    "file": file,
                    "access_allowed": matched_user["access_allowed"]
                }
                files.append(f)

        employee["files"] = files
    return employees

# Method for determining an employees risk and returning the files, if any
def determine_employee_risk_from_violated_files(db: Session, employees: list):
    employees_list = get_employee_violated_files(db, employees)
    
    for employee in employees_list:
        print(employee)
        files = employee["files"]

        # Case 1: no files
        if len(files) == 0:
            employee["files"] = {"id": 1, "status": "No Files Found", "flagged_files": []}
            continue
        
        has_true = False
        has_false = False
        all_none = True

        flagged_files = []

        for f in files:
            access = f.get("access_allowed")

            if access is False:
                has_false = True
                flagged_files.append(f) 

            elif access is True:
                has_true = True
                all_none = False

            elif access is None:
                continue

        # Case 2: all None
        if all(access.get("access_allowed") is None for access in files):
            employee["files"] = {"id": 2, "status": "No Files Scanned", "flagged_files": []}

        # Case 3: any false overrides everything
        elif has_false:
            employee["files"] = {"id": 3, "status": "Risk Detected", "flagged_files": flagged_files}

        # Case 4: at least one true, no false
        elif has_true:
            employee["files"] = {"id": 4, "status": "No Risk Detected", "flagged_files": []}
    
    return employees_list


# INTERNAL HELPER METHOD:
# Method for getting all employees with access to a file from preloaded data
def get_file_employees_with_access_from_data(db: Session, fetched_employees_records: list, has_been_scanned: bool, latest_scan_results: list):
    # Build employees dictionary from fetched employees records
    employees = build_employees_from_records(fetched_employees_records)

    # If file has not been scanned yet, access cannot be evaluated
    if not has_been_scanned:
        # Set every employee's access allowed to 'None' which will display a '?' in the front-end
        for employee in employees.values():
            employee["access_allowed"] = None

        return list(employees.values())

    # Evaluate each employee's access
    for employee in employees.values():
        evaluate_employee_access(db, employee, latest_scan_results)

    return list(employees.values())


# Method for getting the 10 highest risk files
def get_highest_risk_files(db: Session, limit: int, offset: int):
    files = ingestion_repository.get_all_files(db=db)

    # Get file id of every fetched files and put into list
    file_ids = [file.ingestion_file_id for file in files]

    # Get all scan results and employee records in bulk so that only one call is performed instead of one PER file
    latest_scan_results_by_file = scanning_service.get_latest_scan_results_for_files(db=db, file_ids=file_ids)

    # Get all scan statuses by files for all file ids
    scan_status_by_file = scanning_service.get_scan_statuses_for_all_files(db=db, file_ids=file_ids)

    # Get all employees with access for all file ids
    employee_access_by_file = repository.get_employees_with_access_for_files(db=db, file_ids=file_ids)

    highest_risk_files = []

    # Iterate through every file and get its risk details and append to list
    for file in files:
        file_id = file.ingestion_file_id

        latest_scan_results = latest_scan_results_by_file.get(file_id, [])
        employees_with_access = employee_access_by_file.get(file_id, [])
        has_been_scanned = scan_status_by_file.get(file_id, False)

        file_risk_details = get_file_risk_details_from_data(
                db=db, 
                file_id=file.ingestion_file_id, 
                file_name=file.name,
                latest_scan_results=latest_scan_results,
                fetched_employees_records=employees_with_access,
                has_been_scanned=has_been_scanned
            )

        highest_risk_files.append(file_risk_details)

    # Sort list by risk score from highest to lowest
    highest_risk_files.sort(key=attrgetter("risk_score"), reverse=True)

    # Calculate total (to be used for pagination)
    total_files = len(highest_risk_files)

    # Return the highest risk files with offset for pagination
    return PaginatedFileRiskDetailsResponse(
        items= highest_risk_files[offset: offset + limit],
        total=total_files,
        limit=limit,
        offset=offset
    )


# Method for getting a file's risk details from preloaded data
def get_file_risk_details_from_data(db: Session, file_id: int, file_name: str, latest_scan_results: list, fetched_employees_records: list, has_been_scanned: bool):
    employees_with_access = get_file_employees_with_access_from_data(
        db=db, 
        fetched_employees_records=fetched_employees_records,
        has_been_scanned=has_been_scanned,
        latest_scan_results=latest_scan_results)

    # Sum the number of 'counts' of every detection result from latest_scan_results
    detection_count = sum(result["count"] for result in latest_scan_results)

    employees_with_access_count = len(employees_with_access)
    valid_access_count = 0
    invalid_access_count = 0

    # Iterate through every employee and check 'access_allowed' boolean value and increment valid or invalid
    # access count variables
    for employee in employees_with_access:
        if employee["access_allowed"] is True:
            valid_access_count += 1
        elif employee["access_allowed"] is False:
            invalid_access_count += 1

    # Calculate the valid and invalid access percentages
    if employees_with_access_count > 0:
        valid_access_percentage = (valid_access_count / employees_with_access_count) * 100
        invalid_access_percentage = (invalid_access_count / employees_with_access_count) * 100
    else:
        valid_access_percentage = 0.0
        invalid_access_percentage = 0.0

    # Calculate a 'risk score' to help determine the highest risk files when listed
    risk_score = ((invalid_access_count * 2) +  invalid_access_percentage + (detection_count * 0.05))

    return FileRiskDetailsResponse(
        file_id=file_id,
        file_name=file_name,
        employees_with_access_count=employees_with_access_count,
        valid_access_count=valid_access_count,
        invalid_access_count=invalid_access_count,
        valid_access_percentage=round(valid_access_percentage, 2),
        invalid_access_percentage=round(invalid_access_percentage, 2),
        detection_count=detection_count,
        risk_score=round(risk_score, 2),
    )


# Method for building employees dictionary from fetched employee records
def build_employees_from_records(fetched_employees_records):
    employees = {}

    # Iterate through every fetched employee and append to employees dictionary
    for fetched_employee in fetched_employees_records:
        if fetched_employee.user_id not in employees:
            employees[fetched_employee.user_id] = {
                "user_id": fetched_employee.user_id,
                "name": f"{fetched_employee.firstname} {fetched_employee.surname}",
                "email": fetched_employee.email,
                "roles": [],
                "access_allowed": True,
                "last_sent": None,
                "failed_detections": []
            }

        if fetched_employee.role_name and fetched_employee.role_name not in employees[fetched_employee.user_id]["roles"]:
            employees[fetched_employee.user_id]["roles"].append(fetched_employee.role_name)
        
    return employees


# Method for evaluating an employee's access to the file based on its latest scan results
def evaluate_employee_access(db: Session, employee: dict, latest_scan_results: list[dict]):
    role_ids = repository.get_user_role_ids(db=db, user_id=employee["user_id"])

    # If user has no roles, append no_roles_assigned as the violation
    if not role_ids:
        employee["access_allowed"] = False
        employee["failed_detections"].append({
            "subcategory": "NO_ROLES_ASSIGNED",
            "count": None,
            "threshold": None
        })
        return

    # Build the most permissive thresholds considering all employee's role
    effective_thresholds = build_effective_thresholds(db=db, role_ids=role_ids)

    # Get the detections which violate the employee's most effective thresholds
    failed_detections = get_failed_detections(
        latest_scan_results=latest_scan_results,
        effective_thresholds=effective_thresholds
    )

    employee["failed_detections"].extend(failed_detections)
    employee["access_allowed"] = len(employee["failed_detections"]) == 0


# Method for building effective thresholds
# This is to determine the most permissive thresholds while considering 
# all of the employee's roles (since an employee might have multiple)
def build_effective_thresholds(db: Session, role_ids: list[int]):
    effective_thresholds = {}

    for role_id in role_ids:
        permissions = repository.get_role_permissions(db=db, role_id=role_id)

        for permission in permissions:
            subcategory = permission.subcategory
            threshold = permission.threshold

            if subcategory not in effective_thresholds:
                effective_thresholds[subcategory] = threshold
            else:
                effective_thresholds[subcategory] = max(effective_thresholds[subcategory], threshold)

    return effective_thresholds


# Method for getting detections which violate the employee's thresholds per each subcategory
def get_failed_detections(latest_scan_results: list[dict], effective_thresholds: dict):
    failed_detections = []

    for detection in latest_scan_results:
        subcategory = detection["subcategory"]
        detection_count = detection["count"]
        threshold = effective_thresholds.get(subcategory)

        if threshold is not None and detection_count > threshold:
            failed_detections.append({
                "subcategory": subcategory,
                "count": detection_count,
                "threshold": threshold
            })

    return failed_detections


# Method for processing the data before it is used in the email template
async def process_data_for_violation_email_template(db: Session, admin_id: int, employee: SendViolationsEmailRequest):
    user = test_route(admin_id, db)
    now = datetime.now()
    detections = employee.employee.failed_detections
    all_detections = []

    for detection in detections:
        dict = {}
        category = get_category_by_subcategory_name(db, detection.subcategory)
        dict["subcategory"] = detection.subcategory
        dict["count"] = detection.count
        dict["threshold"] = detection.threshold
        dict["category"] = category.name
        all_detections.append(dict)

    return await send_email_with_violations(db, user, employee, all_detections, now)


# Method for sending the email containing the violations
async def send_email_with_violations(db: Session, admin: User, employee: SendViolationsEmailRequest, detection_list: list, now: datetime):
    template = f"""
        <html>
        <body style="margin:0; padding:0; font-family:Arial, sans-serif; background-color:#f5f5f5;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; background:#ffffff;">

            <!-- Header -->
            <tr>
                <td align="center" style="padding:20px;">
                <h2 style="margin:0; color:#333333;">Risk Detection Alert</h2>
                </td>
            </tr>

            <!-- Intro -->
            <tr>
                <td style="padding:20px;">
                <p style="font-size:14px; color:#333333;">
                    Hi {employee.employee.name},
                </p>

                <p style="font-size:14px; color:#333333;">
                    The Data Trust Engine has identified files in your possession that may not align with your current access permissions.
                    Please review the following detections and take appropriate action.
                </p>
                </td>
            </tr>

            <!-- Detections Section -->
            <tr>
                <td style="padding:0 20px 20px 20px;">
        """

    # Loop through files
    template += f"""
    <h3 style="font-size:16px; color:#222222; margin-top:20px;">
        Detections identified for: <span style="color:#007bff;">{employee.file_name}</span>
    </h3>
    """

    # Group detections by category
    grouped = {}
    for detections in detection_list:
        category = detections.get("category", "Other")
        grouped.setdefault(category, []).append(detections)

    # Loop through categories
    for category, items in grouped.items():
        template += f"""
            <h4 style="font-size:14px; color:#333333; margin-top:25px;">
                {category} Information
            </h4>

            <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse:collapse; margin-top:5px;">
                <tr style="background-color:#f0f0f0; text-align:left;">
                    <th style="border:1px solid #dddddd; font-size:13px;">Subcategory</th>
                    <th style="border:1px solid #dddddd; font-size:13px;">Detections</th>
                    <th style="border:1px solid #dddddd; font-size:13px;">Threshold</th>
                </tr>
        """

        for d in items:
            template += f"""
                <tr>
                    <td style="border:1px solid #dddddd; font-size:13px;">
                        {d.get("subcategory")}
                    </td>
                    <td style="border:1px solid #dddddd; font-size:13px; color:#d9534f; font-weight:bold;">
                        {d.get("count")}
                    </td>
                    <td style="border:1px solid #dddddd; font-size:13px;">
                        {d.get("threshold")}
                    </td>
                </tr>
            """

        template += """
            </table>
        """

    template += f"""
            </td>
        </tr>

        <!-- Footer -->
        <tr>
            <td style="padding:20px;">
            <p style="font-size:14px; color:#333333;">
                Please ensure any sensitive or restricted data is handled in accordance with company policies.
            </p>

            <p style="font-size:14px; color:#333333;">
                Best regards, <br/><br/>
                <strong>{admin.firstname} {admin.surname}</strong>
            </p>
            </td>
        </tr>

        <tr>
            <td style="padding:15px; font-size:12px; color:#777777; text-align:center;">
            If you believe this was flagged in error, please contact your administrator.
            </td>
        </tr>

        </table>
      </body>
    </html>
    """

    message = MessageSchema(
        subject="Action Required: Unauthorized File Access Identified",
        recipients=[employee.employee.email], 
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    if (check_admin_cooldown_for_sending_email(db, now, employee, admin.user_id) == True):

        repository.create_violation_email_record(db, now, admin.user_id, employee.employee.user_id)
        await fm.send_message(message)
        return True
    
    return check_admin_cooldown_for_sending_email(db, now, employee, admin.user_id)


# Method for checking whether admin is able to send an email (cooldown)
def check_admin_cooldown_for_sending_email(db: Session, time_now: datetime, employee: SendViolationsEmailRequest, admin_id: int):
    cooldown = timedelta(minutes=1)

    latest_email = repository.get_latest_violation_email_for_cooldown(db, admin_id, employee.employee.user_id)
    if latest_email is None:
        return True
    
    time_difference = time_now - latest_email.created_at
    if(time_difference < cooldown):
        return "cooldown"
        
    return True