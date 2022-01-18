"""
Module containing class for DepartmentAPI resource testing
"""

# pylint: disable=C0103, no-member
import uuid

from flask import url_for

from department_app.test.conftest import BaseTest, logger
from department_app.models import Department


class DepartmentAPITest(BaseTest):
    """
    Class for department api tests
    """
    def test_departmentapi_get(self):
        logger.info("Testing DepartmentAPI get method")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()

        response = self.app.get(url_for('rest_api.departmentapi', department_id=department1.department_id))
        department_json = response.get_json()
        assert response.status_code == 200
        assert department_json

        response = self.app.get(url_for('rest_api.departmentapi', department_id=''))
        department_json = response.get_json()
        assert response.status_code == 404
        assert not department_json

    def test_departmentapi_put(self):
        logger.info("Testing DepartmentAPI put method")
        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break

        response = self.app.put(url_for('rest_api.departmentapi', department_id=nonexistent_department_id))
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

        response = self.app.put(url_for('rest_api.departmentapi', department_id=''))
        message = response.get_json()
        assert response.status_code == 404
        assert message is None

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
                                data={
                                    'department_name': '',
                                    'department_phone_number': '+384444444444'
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
                                data={
                                    'department_name': 'TEST_DP4',
                                    'department_phone_number': ''
                                })
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id))
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message

        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        department1_id = department1.department_id
        response = self.app.put(url_for('rest_api.departmentapi', department_id=department1.department_id),
                                data={
                                    'department_name': 'TEST_DP4',
                                    'department_phone_number': '+384444444444'
                                })
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message
        department1 = Department.query.get(department1_id)
        assert department1.department_name == 'TEST_DP4'
        assert department1.department_phone_number == '+384444444444'

    def test_departmentapi_delete(self):
        logger.info("Testing DepartmentAPI delete method")
        department1 = Department.query.filter_by(department_name='TEST_DP1').one()
        response = self.app.delete(url_for('rest_api.departmentapi', department_id=department1.department_id))
        message = response.get_json()
        assert response.status_code == 200
        assert 'success' in message
        filtered_departments = Department.query.filter_by(department_name='TEST_DP1').all()
        assert len(filtered_departments) == 0

        while True:
            nonexistent_department_id = uuid.uuid4()
            if all(nonexistent_department_id != department.department_id for department in Department.query.all()):
                break

        response = self.app.delete(url_for('rest_api.departmentapi', department_id=nonexistent_department_id))
        message = response.get_json()
        assert response.status_code == 404
        assert 'error' in message

        response = self.app.delete(url_for('rest_api.departmentapi', department_id=''))
        message = response.get_json()
        assert response.status_code == 404
        assert message is None
