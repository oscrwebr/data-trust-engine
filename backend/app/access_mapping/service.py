from sqlalchemy.orm import Session
from app.access_mapping import repository
from app.ingestion import repository as ingestion_repository
from app.access_mapping.schemas import FileRiskDetailsResponse
from app.scanning.service import get_file_latest_scan_results, check_file_has_scan
from operator import attrgetter


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


# Method for getting the 10 highest risk files
def get_highest_risk_files(db: Session, limit: int, offset: int):
    files = ingestion_repository.get_all_files(db=db)

    # Get file id of every fetched files and put into list
    file_ids = [file.ingestion_file_id for file in files]

    # Fetch all scan results and employee records in bulk so that only one call is performed instead of one PER file
    latest_scan_results_by_files = 

    highest_risk_files = []

    # Iterate through every file and get its risk details and append to list
    for file in files:
        print("file:", file.name)
        file_risk_details = get_file_risk_details(
                db=db, 
                file_id=file.ingestion_file_id, 
                file_name=file.name
            )

        highest_risk_files.append(file_risk_details)

    # Sort list by risk score from highest to lowest
    highest_risk_files.sort(key=attrgetter("risk_score"), reverse=True)

    # Return the highest risk files with offset for pagination
    return highest_risk_files[offset: offset + limit]


# Method for getting a file's risk details
def get_file_risk_details(db: Session, file_id: int, file_name: str):
    latest_scan_results = get_file_latest_scan_results(db=db, file_id=file_id)
    employees_with_access = get_file_employees_with_access(db=db, file_id=file_id)

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