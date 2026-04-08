from app.access_mapping import repository
from sqlalchemy.orm import Session


# Method for getting all employees with access to a file
def get_file_employees_with_access(db: Session, file_id: int):
    records = repository.get_file_employees_with_access(db, file_id)

    employees = {}

    for record in records:
        if record.user_id not in employees:
            employees[record.user_id] = {
                "user_id": record.user_id,
                "name": f"{record.firstname} {record.surname}",
                "email": record.email,
                "roles": []
            }

        if record.role_name and record.role_name not in employees[record.user_id]["roles"]:
            employees[record.user_id]["roles"].append(record.role_name)

    return list(employees.values())