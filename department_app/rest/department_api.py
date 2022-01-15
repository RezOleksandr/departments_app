import re
from uuid import UUID

from flask import request
from flask_restful import Resource
import validators

from department_app.service import get_all_departments, get_department_by_id, create_department, delete_department, \
    update_department
from . import api


class DepartmentsAPI(Resource):
    @staticmethod
    def get():
        departments = get_all_departments()
        departments_dicts = [department.to_dict() for department in departments]
        return departments_dicts, 200

    @staticmethod
    def post():
        try:
            request_data = request.form.to_dict()
            department_name_is_valid = validators.length(request_data['department_name'], min=3, max=32)
            if not department_name_is_valid:
                return {'error': 'department_name is invalid'}, 400
            department_name = request_data['department_name']

            department_phone_number_match = re.match(r'(\+?[\d]{1,3})?\d{10}$', request_data['department_phone_number'])
            if not department_phone_number_match:
                return {'error': 'department_phone_number is invalid'}, 400
            department_phone_number = request_data['department_phone_number']
            create_department(department_name, department_phone_number)
        except KeyError as e:
            return {'error': f'missing parameter {str(e)}'}, 400
        except Exception as e:
            return {'error': f'{type(e)}: {str(e)}'}, 500
        return {'success': 'department has been created'}, 201


class DepartmentAPI(Resource):
    @staticmethod
    def get(department_id: str):
        if not validators.uuid(department_id):
            return {'error': 'department_id is invalid'}, 400
        department = get_department_by_id(UUID(department_id))
        if not department:
            return {'error': 'Not Found'}, 404
        return department.to_dict(), 200

    @staticmethod
    def put(department_id: str):
        department_id_is_valid = validators.uuid(department_id)
        if not department_id_is_valid:
            return {'error': 'department_id is invalid'}, 400

        try:
            request_data = request.form.to_dict()
            if 'department_name' in request_data:
                department_name_is_valid = validators.length(request_data['department_name'], min=3, max=32)
                if not department_name_is_valid:
                    return {'error': 'department_name is invalid'}, 400
                department_name = request_data['department_name']
            else:
                department_name = None

            if 'department_phone_number' in request_data:
                department_phone_number_match = re.match(r'(\+?[\d]{1,3})?\d{10}$',
                                                         request_data['department_phone_number'])
                if not department_phone_number_match:
                    return {'error': 'department_phone_number is invalid'}, 400
                department_phone_number = request_data['department_phone_number']
            else:
                department_phone_number = None

            is_updated = update_department(UUID(department_id), department_name, department_phone_number)
            if not is_updated:
                return {'error': 'Not Found'}, 404
        except KeyError as e:
            return {'error': f'missing parameter {str(e)}'}, 400
        except Exception as e:
            return {'error': f'{type(e)}: {str(e)}'}, 500
        return {'success': 'department has been updated'}, 201

    @staticmethod
    def delete(department_id: str):
        department_id_is_valid = validators.uuid(department_id)
        if not department_id_is_valid:
            return {'error': 'department_id is invalid'}, 400

        is_deleted = delete_department(UUID(department_id))
        if not is_deleted:
            return {'error': 'Not Found'}, 404
        return {'success': 'department has been deleted'}, 200


api.add_resource(DepartmentsAPI, '/departments')
api.add_resource(DepartmentAPI, '/departments/<string:department_id>')
