"""
Module containing class for EmployeeAPI resource testing
"""

# pylint: disable=C0103, no-member
import uuid
from datetime import date, timedelta

from flask import url_for

from department_app.test.conftest import BaseTest, logger
from department_app.models import Department, Employee


class EmployeeAPITest(BaseTest):
    """
    Class for employee api tests
    """
    def test_employeeapi_get(self):
        logger.info("Testing EmployeeAPI get method")
        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()

        response = self.app.get(url_for('rest_api.employeeapi', employee_id=employee1.employee_id))
        employee_json = response.get_json()
        assert response.status_code == 200
        assert employee_json

        response = self.app.get(url_for('rest_api.employeeapi', employee_id=''))
        department_json = response.get_json()
        assert response.status_code == 404
        assert not department_json

    def test_employeeapi_put(self):
        logger.info("Testing EmployeeAPI put method")
        employee2 = Employee.query.filter_by(employee_name='TEST_E2').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()

        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee2.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={})
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message

        response = self.app.put(url_for('rest_api.employeeapi', employee_id=''))
        assert response.status_code == 404

        while True:
            nonexistent_employee_id = uuid.uuid4()
            if all(nonexistent_employee_id != employee.employee_id for employee in Employee.query.all()):
                break

        response = self.app.put(url_for('rest_api.employeeapi', employee_id=nonexistent_employee_id))
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': '',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': '',
                                    'salary': 444,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': '',
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': -1,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': '',
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        department2 = Department.query.filter_by(department_name='TEST_DP2').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': date.today() + timedelta(1),
                                    'department_id': department2.department_id
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': ''
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        response = self.app.put(url_for('rest_api.employeeapi', employee_id=employee1.employee_id),
                                data={
                                    'employee_name': 'TEST_E4',
                                    'position': 'Test Subject 4',
                                    'salary': 444,
                                    'birthdate': date(1994, 4, 14),
                                    'department_id': nonexistent_department_id
                                })
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

    #     response = self.app.put(url_for('rest_api.departmentapi', department_id=''))
    #     message = response.get_json()
    #     assert response.status_code == 404
    #     assert message is None
    #
    #     department1 = Department.query.filter_by(department_name='TEST_DP1').one()
    #     response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
    #                             data={
    #                                 'department_name': '',
    #                                 'department_phone_number': '+384444444444'
    #                             })
    #     message = response.get_json()
    #     assert response.status_code == 400
    #     assert 'error' in message
    #
    #     department1 = Department.query.filter_by(department_name='TEST_DP1').one()
    #     response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
    #                             data={
    #                                 'department_name': 'TEST_DP4',
    #                                 'department_phone_number': ''
    #                             })
    #     message = response.get_json()
    #     assert response.status_code == 400
    #     assert 'error' in message
    #
    #     department1 = Department.query.filter_by(department_name='TEST_DP1').one()
    #     response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id))
    #     message = response.get_json()
    #     assert response.status_code == 201
    #     assert 'success' in message
    #
    #     department1 = Department.query.filter_by(department_name='TEST_DP1').one()
    #     department1_id = department1.department_id
    #     response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
    #                             data={
    #                                 'department_name': 'TEST_DP4',
    #                                 'department_phone_number': '+384444444444'
    #                             })
    #     message = response.get_json()
    #     assert response.status_code == 201
    #     assert 'success' in message
    #     department1 = Department.query.get(department1_id)
    #     assert department1.department_name == 'TEST_DP4'
    #     assert department1.department_phone_number == '+384444444444'

    def test_employeeapi_delete(self):
        logger.info("Testing EmployeeAPI delete method")
        employee1 = Employee.query.filter_by(employee_name='TEST_E1').one()
        response = self.app.delete(url_for('rest_api.employeeapi', employee_id=employee1.employee_id))
        message = response.get_json()
        assert response.status_code == 200
        assert 'success' in message
        filtered_employees = Employee.query.filter_by(employee_name='TEST_E1').all()
        assert len(filtered_employees) == 0

        while True:
            nonexistent_employee_id = uuid.uuid4()
            if all(nonexistent_employee_id != employee.department_id for employee in Employee.query.all()):
                break

        response = self.app.delete(url_for('rest_api.employeeapi', employee_id=nonexistent_employee_id))
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

        response = self.app.delete(url_for('rest_api.employeeapi', employee_id=''))
        message = response.get_json()
        assert response.status_code == 404
        assert message is None
