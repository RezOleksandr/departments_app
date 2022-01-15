import requests
from flask import Blueprint, render_template, request, redirect, url_for, g, current_app


departments = Blueprint('departments', __name__, template_folder='templates')


@departments.route('/departments/', methods=['GET'])
def departments_view():
    response = requests.get(url_for('rest_api.departmentsapi', _external=True))
    departments_json = response.json()
    return render_template('departments.html', departments=departments_json)


@departments.route('/departments/add', methods=['GET'])
def departments_add():
    return render_template('departments_add.html')


@departments.route('/departments/<uuid:department_id>/edit', methods=['GET'])
def departments_edit(department_id):
    response = requests.get(url_for('rest_api.departmentapi', department_id=department_id, _external=True))
    department_json = response.json()
    return render_template('department_edit.html', department=department_json)
