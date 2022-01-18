"""
Module containing class for DepartmentsAPI resource testing
"""

# pylint: disable=C0103, no-member
from flask import url_for

from department_app.test.conftest import BaseTest, logger
from department_app.models import Department


class DepartmentsAPITest(BaseTest):
    """
    Class for departments api tests
    """
    def test_departmentsapi_get(self):
        logger.info("Testing DepartmentsAPI get method")
        response = self.app.get(url_for('rest_api.departmentsapi'))
        departments_json = response.get_json()
        assert response.status_code == 200
        assert len(departments_json) == 3

    def test_departmentsapi_post(self):
        logger.info("Testing DepartmentsAPI post method")
        response = self.app.post(url_for('rest_api.departmentsapi'), data={'department_name': 'TEST_DP4',
                                                                           'department_phone_number': '+384444444444'})
        message = response.get_json()
        assert response.status_code == 201
        assert 'success' in message
        filtered_departments = Department.query.filter_by(department_name='TEST_DP4').all()
        assert len(filtered_departments) == 1

        response = self.app.post(url_for('rest_api.departmentsapi'))
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.post(url_for('rest_api.departmentsapi'), data={'department_name': 'TEST_DP5'})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.post(url_for('rest_api.departmentsapi'), data={'department_name': '',
                                                                           'department_phone_number': '+385555555555'})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message

        response = self.app.post(url_for('rest_api.departmentsapi'), data={'department_name': 'TEST_DP5',
                                                                           'department_phone_number': ''})
        message = response.get_json()
        assert response.status_code == 400
        assert 'error' in message
