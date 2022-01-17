"""
Module containing functions to work with the Employee model
"""

# pylint: disable=no-member
from typing import Union
from datetime import date
from uuid import UUID

from sqlalchemy import and_

from department_app.database import db
from department_app.models import Employee


def get_all_employees() -> list:
    """
    Function returns list of all employees
    :return: list of all employees
    :rtype: list
    """
    employees = Employee.query.all()
    return employees


def get_employee_by_id(employee_id: UUID) -> Union[Employee, bool]:
    """
    Function returns Employee with specified id
    :param employee_id: id of an employee
    :type employee_id: UUID
    :return: Employee if employee exists else False
    :rtype: Employee or bool
    """
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return False
    return employee


def get_employees_with_filter(department_id: Union[UUID, None] = None,
                              start_date: Union[date, None] = None,
                              end_date: Union[date, None] = None) -> list:
    """
    Function returns Employees that are satisfying conditions
    :param department_id: employees department id condition, None if not specified
    :type department_id: UUID or None
    :param start_date: start date condition, None if not specified
    :type start_date: date or None
    :param end_date: end date condition, None if not specified
    :type end_date: date or None
    :return: list of employees that are satisfying conditions
    :rtype: list
    """
    department_filter = (Employee.department_id == department_id) if department_id is not None else True
    start_date_filter = (Employee.birthdate >= start_date) if start_date is not None else True
    end_date_filter = (Employee.birthdate <= end_date) if end_date is not None else True

    filters = (department_filter, start_date_filter, end_date_filter)

    employees = Employee.query.filter(and_(*filters)).all()

    return employees


def create_employee(employee_name: str, position: str, salary: float, birthdate: date, department_id: UUID) -> bool:
    """
    Function creates new Department
    :param employee_name: name of an employee
    :type employee_name: str
    :param position: position of an employee
    :type position: str
    :param salary: salary of an employee
    :type salary: float
    :param birthdate: birthdate of an employee
    :type birthdate: date
    :param department_id: department id of an employee
    :type department_id: UUID
    :return: returns True
    :rtype: bool
    """
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
                    salary: Union[float, None] = None,
                    birthdate: Union[date, None] = None,
                    department_id: Union[UUID, None] = None) -> bool:
    """
    Function updates Employee with specified id
    :param employee_id: id of an employee
    :type employee_id: UUID
    :param employee_name: id of an employee, None if not specified
    :type employee_name: str or None
    :param position: id of an employee, None if not specified
    :type position: str or None
    :param salary: id of an employee, None if not specified
    :type salary: float or None
    :param birthdate: id of an employee, None if not specified
    :type birthdate: date or None
    :param department_id: department id of an employee, None if not specified
    :type department_id: UUID or None
    :return: returns True on success else False
    :rtype: bool
    """
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
    """
    Function deletes Employee with specified id
    :param employee_id: id of an employee
    :type employee_id: UUID
    :return: returns True on success else False
    :rtype: bool
    """
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return False

    db.session.delete(employee)
    db.session.commit()
    return True
