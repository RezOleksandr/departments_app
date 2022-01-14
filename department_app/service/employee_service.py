from typing import Union
from datetime import date
from uuid import UUID

from sqlalchemy import and_

from department_app.database import db
from department_app.models import Employee


def get_all_employees() -> list:
    employees = Employee.query.all()
    return employees


def get_employee_by_id(employee_id: UUID) -> Union[Employee, bool]:
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return False
    return employee


def get_employees_with_filter(department_id: UUID = None, start_date: date = None, end_date: date = None) -> list:
    department_filter = (Employee.department_id == department_id) if department_id is not None else True
    start_date_filter = (Employee.birthdate >= start_date) if start_date is not None else True
    end_date_filter = (Employee.birthdate >= start_date) if end_date is not None else True

    filters = (department_filter, start_date_filter, end_date_filter)

    employees = Employee.query.filter(and_(*filters)).all()

    return employees


def create_employee(employee_name: str, position: str, salary: float, birthdate: date, department_id: UUID) -> bool:
    employee = Employee(employee_name=employee_name,
                        position=position,
                        salary=salary,
                        birthdate=birthdate,
                        department_id=department_id)
    db.session.add(employee)
    db.session.commit()
    return True


def update_employee(employee_id: UUID,
                    employee_name: Union[str, None] = None,
                    position: Union[str, None] = None,
                    salary: Union[str, None] = None,
                    birthdate: Union[str, None] = None,
                    department_id: Union[str, None] = None) -> bool:
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return False

    if employee_name is not None:
        employee.employee_name = employee_name
    if position is not None:
        employee.position = position
    if salary is not None:
        employee.salary = salary
    if birthdate is not None:
        employee.birthdate = birthdate
    if department_id is not None:
        employee.department_id = department_id

    db.session.add(employee)
    db.session.commit()
    return True


def delete_employee(employee_id: UUID) -> bool:
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return False

    db.session.delete(employee)
    db.session.commit()
    return True
