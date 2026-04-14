from sqlalchemy.orm import Session
from app.access_mapping import repository
from app.access_mapping.schemas import conf, SendViolationsEmailRequest
from app.scanning.service import get_file_latest_scan_results, check_file_has_scan
from fastapi_mail import FastMail, MessageSchema
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from app.authentication.models import User


# Method for getting all employees with access to a file
def get_file_employees_with_access(db: Session, file_id: int):
    fetched_employees_records = repository.get_file_employees_with_access(db=db, file_id=file_id)
    has_been_scanned = check_file_has_scan(db=db, file_id=file_id)
    latest_scan_results = get_file_latest_scan_results(db=db, file_id=file_id)

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
        #await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    
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