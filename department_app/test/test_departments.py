"""
Module containing class for Department model testing
"""

# pylint: disable=C0103, no-member
from uuid import UUID

import validators
from sqlalchemy.exc import IntegrityError

from department_app.test.conftest import BaseTest, logger
from department_app.database import db
from department_app.models import Department


class DepartmentsTest(BaseTest):
    """
    Class for department model tests
    """

    @staticmethod
    def test_department_creation():
        logger.info("Testing department creation")
        departments = Department.query.all()
        assert departments is not None
        assert len(departments) == 3

        department1 = departments[0]
        assert department1 in db.session
        assert validators.uuid(department1.department_id)
        assert isinstance(department1.department_id, UUID)
        assert isinstance(department1.department_name, str)
        assert isinstance(department1.department_phone_number, str)

    @staticmethod
    def test_department_not_unique_uuid():
        logger.info("Testing creation of departments with the same id")
        department1 = Department.query.all()[0]
        department4 = Department(department_id=department1.department_id)
        db.session.add(department4)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            assert True

    @staticmethod
    def test_department_employees():
        logger.info("Testing department employees")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()

        assert department1.employees is not None
        assert isinstance(department1.number_of_employees, int)
        assert len(department1.employees) == department1.number_of_employees == 2
        assert isinstance(department1.average_salary, float)
        assert round(department1.average_salary, 3) == round((111 + 222) / 2, 3)

        department3 = Department.query.filter_by(department_name='TEST_DP3').one()
        assert department3.average_salary == 0

    @staticmethod
    def test_department_to_dict():
        logger.info("Testing department to_dict method")
        department1 = Department.query.all()[0]
        department1_dict = department1.to_dict()

        expected_dict_keys = ('department_id', 'department_name', 'department_phone_number', 'number_of_employees',
                              'average_salary', 'employees')

        assert isinstance(department1_dict, dict)
        assert all(key in department1_dict for key in expected_dict_keys)
