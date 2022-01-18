"""
Module containing class for EmployeesAPI resource testing
"""

# pylint: disable=C0103, no-member
import uuid

from flask import url_for
from datetime import date, timedelta

from department_app.test.conftest import BaseTest, logger
from department_app.models import Department, Employee


class EmployeesAPITest(BaseTest):
    """
    Class for employees api tests
    """
    def test_employeesapi_get(self):
        logger.info("Testing EmployeesAPI get method")

        response = self.app.get(url_for('rest_api.employeesapi'))
        employees_json = response.get_json()
        assert response.status_code == 200
        assert len(employees_json) == 3

        response = self.app.get(url_for('rest_api.employeesapi'), query_string={'a': 'b'})
        employees_json = response.get_json()
        assert response.status_code == 200
        assert len(employees_json) == 3

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'department_id': ''})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'department_id': nonexistent_department_id})
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'start_date': ''})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'start_date': date.today() + timedelta(1)})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'end_date': ''})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'end_date': date.today() + timedelta(1)})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={'department_id': department1.department_id})
        employees_json = response.get_json()
        assert response.status_code == 200
        assert len(employees_json) == 2
        assert employees_json[0]['department_id'] == str(department1.department_id)

        response = self.app.get(url_for('rest_api.employeesapi'),
                                query_string={
                                    'start_date': date(1992, 1, 1),
                                    'end_date': date(1992, 12, 31)
                                })
        employees_json = response.get_json()
        assert response.status_code == 200
        assert len(employees_json) == 1
        assert employees_json[0]['birthdate'] == str(date(1992, 2, 12))

    def test_employeesapi_post(self):
        logger.info("Testing EmployeesAPI post method")

        response = self.app.post(url_for('rest_api.employeesapi'))
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.post(url_for('rest_api.employeesapi'), data={})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message
        filtered_employees = Employee.query.filter_by(employee_name='TEST_E4').all()
        assert len(filtered_employees) == 1

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': '',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': '',
                                                                         'salary': 444,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': '',
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': -1,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': '',
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': date.today() + timedelta(1),
                                                                         'department_id': department1.department_id})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': ''})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break
        response = self.app.post(url_for('rest_api.employeesapi'), data={'employee_name': 'TEST_E4',
                                                                         'position': 'Test Subject 4',
                                                                         'salary': 444,
                                                                         'birthdate': date(1994, 4, 14),
                                                                         'department_id': nonexistent_department_id})
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message






