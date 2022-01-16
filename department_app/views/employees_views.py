"""
Module containing employees blueprint and functions
"""

from uuid import UUID

import requests
from flask import Blueprint, render_template, request, url_for

employees = Blueprint('employees', __name__, template_folder='templates')


@employees.route('/employees/', methods=['GET'])
def employees_view() -> str:
    """
    Renders and returns web page with employees that satisfy filtering options received from request args
    :return: rendered HTML page
    :rtype: str
    """
    request_data = request.args.to_dict()
    if request_data is not None:
        if 'department_id' in request_data and request_data['department_id']:
            department_id = request_data['department_id']
        else:
            department_id = None
        if 'start_date' in request_data and request_data['start_date']:
            start_date = request_data['start_date']
        else:
            start_date = None
        if 'end_date' in request_data and request_data['end_date']:
            end_date = request_data['end_date']
        else:
            end_date = None

        response = requests.get(url_for('rest_api.employeesapi', _external=True,
                                        department_id=department_id,
                                        start_date=start_date,
                                        end_date=end_date))
    else:
        response = requests.get(url_for('rest_api.employeesapi', _external=True))
    employees_json = response.json()
    response = requests.get(url_for('rest_api.departmentsapi', _external=True))
    departments_json = response.json()
    return render_template('employees.html', employees=employees_json, departments=departments_json)


@employees.route('/employees/add', methods=['GET'])
def employees_add() -> str:
    """
    Renders and returns web page used to add an employee
    :return: rendered HTML page
    :rtype: str
    """
    response = requests.get(url_for('rest_api.departmentsapi', _external=True))
    departments_json = response.json()
    return render_template('employees_add.html', departments=departments_json)


@employees.route('/employees/<uuid:employee_id>/edit', methods=['GET'])
def employees_edit(employee_id: UUID):
    """
    Renders and returns web page used to edit data of an employee with specified id
    :param employee_id: id of an employee
    :type employee_id: UUID
    :return: rendered HTML page
    :rtype: str
    """
    response = requests.get(url_for('rest_api.employeeapi', employee_id=employee_id, _external=True))
    employee_json = response.json()
    response = requests.get(url_for('rest_api.departmentsapi', _external=True))
    departments_json = response.json()
    return render_template('employee_edit.html', employee=employee_json, departments=departments_json)
