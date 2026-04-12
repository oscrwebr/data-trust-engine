from sqlalchemy.orm import Session
from app.access_mapping import repository
from app.scanning.service import get_file_latest_scan_results, check_file_has_scan


# Method for getting all employees with access to a file
def get_file_employees_with_access(db: Session, file_id: int):
    fetched_employees_records = repository.get_file_employees_with_access(db=db, file_id=file_id)
    has_been_scanned = check_file_has_scan(db=db, file_id=file_id)
    latest_scan_results = get_file_latest_scan_results(db=db, file_id=file_id)

    # Build employees dictionary from fetched employees records
    employees = build_employees_from_records(fetched_employees_records)

    # If file has not been scanned yet, access cannot be evaluated
    if not has_been_scanned:
        for employee in employees.values():
            employee["access_allowed"] = None

        return list(employees.values())

    # Evaluate each employee's access
    for employee in employees.values():
        role_ids = repository.get_user_role_ids(db=db, user_id=employee["user_id"])

        # No roles means they should not have access
        if not role_ids:
            employee["access_allowed"] = False
            employee["failed_detections"].append({
                "subcategory": "NO_ROLES_ASSIGNED",
                "count": None,
                "threshold": None
            })
            continue

        effective_thresholds = {}

        # Build the most permissive threshold per subcategory across all roles (employees might have multiple roles)
        for role_id in role_ids:
            permissions = repository.get_role_permissions(db=db, role_id=role_id)

            for permission in permissions:
                subcategory = permission.subcategory
                threshold = permission.threshold

                # Append or update the subcategory with threshold to keep most permissive
                if subcategory not in effective_thresholds:
                    effective_thresholds[subcategory] = threshold
                else:
                    effective_thresholds[subcategory] = max(effective_thresholds[subcategory], threshold)

        # Compare the file's detections againsst employee's most permissive thresholds
        for detection in latest_scan_results:
            subcategory = detection["subcategory"]
            detection_count = detection["count"]
            threshold = effective_thresholds.get(subcategory)

            # Check if the detection count is greater than the threshold and append failed detection if so
            if threshold is not None and detection_count > threshold:
                employee["failed_detections"].append({
                    "subcategory": subcategory,
                    "count": detection["count"],
                    "threshold": threshold
                })

        if len(employee["failed_detections"]) == 0:
            employee["access_allowed"] = True
        else:
            employee["access_allowed"] = False

    return list(employees.values())



# Method for building employees dictionary from fetched employee records
def build_employees_from_records(fetched_employees_records):
    employees = {}

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