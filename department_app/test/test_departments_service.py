"""
Module containing class for Department model testing
"""

# pylint: disable=C0103, no-member
import uuid

from department_app.test.conftest import BaseTest, logger
from department_app.models import Department
from department_app.service import get_all_departments, get_department_by_id, create_department, update_department, \
    delete_department


class DepartmentsServiceTest(BaseTest):
    """
    Class for departments service test
    """
    @staticmethod
    def test_get_all_departments():
        logger.info("Testing get_all_departments method")
        all_departments = get_all_departments()
        all_departments_from_query = Department.query.all()
        assert isinstance(all_departments, list)
        assert all_departments == all_departments_from_query

    @staticmethod
    def test_get_department_by_id():
        logger.info("Testing get_department_by_id method")
        department1_from_query = Department.query.filter_by(department_name='TEST_DP1').one()
        department1 = get_department_by_id(department1_from_query.department_id)
        assert department1 == department1_from_query

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        assert not get_department_by_id(nonexistent_department_id)

    @staticmethod
    def test_create_department():
        logger.info("Testing create_department method")
        department4 = create_department(department_name='TEST_DP4', department_phone_number="+389999999999")
        assert department4
        filtered_departments_query = Department.query.filter_by(department_name='TEST_DP4')
        assert filtered_departments_query
        department4_from_query = filtered_departments_query.one()
        assert department4_from_query.department_name == 'TEST_DP4'
        assert department4_from_query.department_phone_number == '+389999999999'

    @staticmethod
    def test_update_department():
        logger.info("Testing update_department method")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()

        update_result = update_department(department1.department_id)
        assert update_result
        assert department1.department_name == 'TEST_DP1'
        assert department1.department_phone_number == '+381111111111'

        update_department(department1.department_id, department_name='TEST_DP4',
                          department_phone_number='+382222222222')
        assert department1.department_name == 'TEST_DP4'
        assert department1.department_phone_number == '+382222222222'

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        assert not update_department(nonexistent_department_id)

    @staticmethod
    def test_delete_department():
        logger.info("Testing delete_department method")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()

        delete_result = delete_department(department1.department_id)
        assert delete_result
        assert not Department.query.get(department1.department_id)

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        assert not delete_department(nonexistent_department_id)

