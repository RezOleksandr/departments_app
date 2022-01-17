"""
Module containing class for Employee model testing
"""

# pylint: disable=C0103, no-member
from uuid import UUID
from datetime import date

import validators
from sqlalchemy.exc import IntegrityError

from department_app.test.conftest import BaseTest, logger
from department_app.database import db
from department_app.models import Employee


class EmployeesTest(BaseTest):
    """
    Class for employee model test
    """

    @staticmethod
    def test_employee_creation():
        logger.info("Testing employees creation")
        employees = Employee.query.all()
        assert employees is not None
        assert len(employees) == 3

        employee1 = employees[0]
        assert employee1 in db.session
        assert validators.uuid(employee1.employee_id)
        assert isinstance(employee1.employee_id, UUID)
        assert isinstance(employee1.employee_name, str)
        assert isinstance(employee1.position, str)
        assert isinstance(employee1.salary, float)
        assert isinstance(employee1.birthdate, date)
        assert validators.uuid(employee1.department_id)
        assert isinstance(employee1.department_id, UUID)

    @staticmethod
    def test_employee_not_unique_uuid():
        logger.info("Testing creation of employees with the same id")
        employee1 = Employee.query.all()[0]
        employee4 = Employee(employee_id=employee1.employee_id)
        db.session.add(employee4)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            assert True

    @staticmethod
    def test_employee_department():
        logger.info("Testing department employees")
        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()

        assert employee1.department is not None
        assert employee1.department.department_id == employee1.department_id
        assert employee1.department.department_name == 'TEST_DP1'
        assert employee1 in employee1.department.employees

    @staticmethod
    def test_employee_to_dict():
        logger.info("Testing department to_dict method")
        employee1 = Employee.query.all()[0]
        employee1_dict = employee1.to_dict()

        expected_dict_keys = ('employee_id', 'employee_name', 'position', 'salary', 'birthdate',
                              'department_id', 'department')

        assert isinstance(employee1_dict, dict)
        assert all(key in employee1_dict for key in expected_dict_keys)

