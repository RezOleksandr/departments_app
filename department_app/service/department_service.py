"""
Module containing functions to work with the Department model
"""

# pylint: disable=no-member
from typing import Union

from uuid import UUID
from department_app.database import db
from department_app.models import Department


def get_all_departments() -> list:
    """
    Function returns list of all departments
    :return: list of all departments
    :rtype: list
    """
    departments = Department.query.all()
    return departments


def get_department_by_id(department_id: UUID) -> Union[Department, bool]:
    """
    Function returns Department with specified id
    :param department_id: id of a department
    :type department_id: UUID
    :return: Department if department exists else False
    :rtype: Department or bool
    """
    department = db.session.get(Department, department_id)
    if not department:
        return False

    return department


def create_department(department_name: str, department_phone_number: str) -> bool:
    """
    Function creates new Department
    :param department_name: name of a department
    :type department_name: str
    :param department_phone_number: phone number of a department
    :type department_phone_number: str
    :return: returns True
    :rtype: bool
    """
    department = Department(department_name=department_name, department_phone_number=department_phone_number)
    db.session.add(department)
    db.session.commit()
    return True


def update_department(department_id: UUID,
                      department_name: Union[str, None] = None,
                      department_phone_number: Union[str, None] = None) -> bool:
    """
    Function updates Department with specified id
    :param department_id: id of a department
    :type department_id: UUID
    :param department_name: name of a department, None if not specified
    :type department_name: str or None
    :param department_phone_number: phone number of a department, None if not specified
    :type department_phone_number: str or None
    :return: returns True on success else False
    :rtype: bool
    """
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
    """
    Function deletes Department with specified id
    :param department_id: id of a department
    :type department_id: UUID
    :return: returns True on success else False
    :rtype: bool
    """
    department = db.session.get(Department, department_id)
    if not department:
        return False

    db.session.delete(department)
    db.session.commit()
    return True
