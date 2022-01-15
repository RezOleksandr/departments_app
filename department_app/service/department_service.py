from typing import Union

from uuid import UUID
from department_app.database import db
from department_app.models import Department


def get_all_departments() -> list:
    departments = Department.query.all()
    return departments


def get_department_by_id(department_id: UUID) -> Union[Department, bool]:
    department = db.session.get(Department, department_id)
    if not department:
        return False

    return department


def create_department(department_name: str, department_phone_number: str) -> bool:
    department = Department(department_name=department_name, department_phone_number=department_phone_number)
    db.session.add(department)
    db.session.commit()
    return True


def update_department(department_id: UUID,
                      department_name: Union[str, None] = None,
                      department_phone_number: Union[str, None] = None) -> bool:
    department = db.session.get(Department, department_id)
    if not department:
        return False

    if department_name is not None:
        department.department_name = department_name
    if department_phone_number is not None:
        department.department_phone_number = department_phone_number

    db.session.add(department)
    db.session.commit()
    return True


def delete_department(department_id: UUID) -> bool:
    department = db.session.get(Department, department_id)
    if not department:
        return False

    db.session.delete(department)
    db.session.commit()
    return True
