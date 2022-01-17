"""
Module containing class for Department model testing
"""

# pylint: disable=C0103, no-member
import uuid
from datetime import date

from department_app.test.conftest import BaseTest, logger
from department_app.models import Employee, Department
from department_app.service import get_all_employees, get_employees_with_filter, get_employee_by_id, create_employee, \
    update_employee, delete_employee


class DepartmentsServiceTest(BaseTest):
    """
    Class for employees service test
    """
    @staticmethod
    def test_get_all_employees():
        logger.info("Testing get_all_employees method")
        all_employees = get_all_employees()
        all_employees_from_query = Employee.query.all()
        assert isinstance(all_employees, list)
        assert all_employees == all_employees_from_query

    @staticmethod
    def test_get_employees_with_filter():
        logger.info("Testing get_employees_with_filter method")
        all_employees_from_query = Employee.query.all()
        filtered_employees = get_employees_with_filter()
        assert isinstance(filtered_employees, list)
        assert all_employees_from_query == filtered_employees

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        filtered_employees = get_employees_with_filter(department_id=department1.department_id)
        filtered_employees_from_query = Employee.query.filter_by(department_id=department1.department_id).all()
        assert filtered_employees == filtered_employees_from_query

        filtered_employees = get_employees_with_filter(start_date=date(1991, 12, 31), end_date=date(1992, 12, 31))
        filtered_employees_from_query = Employee.query.filter_by(birthdate=date(1992, 2, 12)).all()
        assert filtered_employees == filtered_employees_from_query

    @staticmethod
    def test_get_employee_by_id():
        logger.info("Testing get_employee_by_id method")
        employee1_from_query = Employee.query.filter_by(employee_name='TEST_E1').one()
        employee1 = get_employee_by_id(employee1_from_query.employee_id)
        assert employee1 == employee1_from_query

        while True:
            nonexistent_employee_id = uuid.uuid4()
            if all(nonexistent_employee_id != employee.employee_id for employee in Employee.query.all()):
                break
        assert not get_employee_by_id(nonexistent_employee_id)

    @staticmethod
    def test_create_employee():
        logger.info("Testing create_employee method")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        employee4 = create_employee(employee_name='TEST_E4', position='Test Subject 4', salary=444,
                                    birthdate=date(2004, 4, 4), department_id=department1.department_id)
        assert employee4
        filtered_employees_query = Employee.query.filter_by(employee_name='TEST_E4')
        assert filtered_employees_query
        employee4_from_query = filtered_employees_query.one()
        assert employee4_from_query.employee_name == 'TEST_E4'
        assert employee4_from_query.position == 'Test Subject 4'
        assert employee4_from_query.salary == 444
        assert employee4_from_query.birthdate == date(2004, 4, 4)
        assert employee4_from_query.department_id == department1.department_id

    @staticmethod
    def test_update_employee():
        logger.info("Testing update_employee method")
        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()

        update_result = update_employee(employee1.employee_id)
        assert update_result
        assert employee1.employee_name == 'TEST_E1'
        assert employee1.position == 'Test Subject 1'
        assert employee1.salary == 111
        assert employee1.birthdate == date(1991, 1, 11)
        assert employee1.department_id == department1.department_id

        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        update_employee(employee1.employee_id, employee_name='TEST_E4', position='Test Subject 4', salary=444,
                        birthdate=date(1994, 4, 14), department_id=department2.department_id)
        assert employee1.employee_name == 'TEST_E4'
        assert employee1.position == 'Test Subject 4'
        assert employee1.salary == 444
        assert employee1.birthdate == date(1994, 4, 14)
        assert employee1.department_id == department2.department_id

        while True:
            nonexistent_employee_id = uuid.uuid4()
            if all(nonexistent_employee_id != employee.employee_id for employee in Employee.query.all()):
                break
        assert not update_employee(nonexistent_employee_id)

    @staticmethod
    def test_delete_employee():
        logger.info("Testing delete_employee method")
        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()

        delete_result = delete_employee(employee1.employee_id)
        assert delete_result
        assert not Employee.query.get(employee1.employee_id)

        while True:
            nonexistent_employee_id = uuid.uuid4()
            if all(nonexistent_employee_id != employee.employee_id for employee in Employee.query.all()):
                break
        assert not delete_employee(nonexistent_employee_id)

