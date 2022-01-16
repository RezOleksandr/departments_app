from flask import Blueprint
from flask_restful import Api

from .department_api import DepartmentsAPI, DepartmentAPI
from .employee_api import EmployeesAPI, EmployeeAPI


rest_api = Blueprint('rest_api', __name__)
api = Api(rest_api)

api.add_resource(DepartmentsAPI, '/departments')
api.add_resource(DepartmentAPI, '/departments/<uuid:department_id>')
api.add_resource(EmployeesAPI, '/employees')
api.add_resource(EmployeeAPI, '/employees/<uuid:employee_id>')
