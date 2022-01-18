"""
Module containing class for Employees views testing
"""

# pylint: disable=C0103, no-member
import http
import uuid

from flask import current_app, url_for

from department_app.test.conftest import BaseTest, logger
from department_app.views import departments
from department_app.views.departments_views import departments_view, departments_add, departments_edit
from department_app.service import get_all_departments, get_department_by_id, create_department, update_department, \
    delete_department


class EmployeesViewsTest(BaseTest):
    """
    Class for employees views tests
    """
