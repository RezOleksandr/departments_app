"""
Module containing departments blueprint and functions
"""

from uuid import UUID

import requests
from flask import Blueprint, render_template, url_for


departments = Blueprint('departments', __name__, template_folder='templates')


@departments.route('/departments/', methods=['GET'])
def departments_view() -> str:
    """
    Renders and returns web page with all departments
    :return: rendered HTML page
    :rtype: str
    """
    response = requests.get(url_for('rest_api.departmentsapi', _external=True))
    departments_json = response.json()
    return render_template('departments.html', departments=departments_json)


@departments.route('/departments/add', methods=['GET'])
def departments_add() -> str:
    """
    Renders and returns web page used to add a department
    :return: rendered HTML page
    :rtype: str
    """
    return render_template('departments_add.html')


@departments.route('/departments/<uuid:department_id>/edit', methods=['GET'])
def departments_edit(department_id: UUID) -> str:
    """
    Renders and returns web page used to edit data of a department with specified id
    :param department_id: id of a department
    :type department_id: UUID
    :return: rendered HTML page
    :rtype: str
    """
    response = requests.get(url_for('rest_api.departmentapi', department_id=department_id, _external=True))
    department_json = response.json()
    return render_template('department_edit.html', department=department_json)
