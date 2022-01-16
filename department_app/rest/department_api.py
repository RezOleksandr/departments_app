"""
Module containing REST API resource classes to work with departments
"""
import re
from uuid import UUID
from typing import Tuple

from flask import request
from flask_restful import Resource
import validators

from department_app.service import get_all_departments, get_department_by_id, create_department, delete_department, \
    update_department


class DepartmentsAPI(Resource):
    """
    Resource class to work with departments
    """
    @staticmethod
    def get() -> Tuple[list, int]:
        """
        Returns list of all departments in the database and status code
        :return: tuple containing list of departments and status code
        :rtype: Tuple[list, int]
        """
        departments = get_all_departments()
        departments_dicts = [department.to_dict() for department in departments]
        return departments_dicts, 200

    @staticmethod
    def post() -> Tuple[dict, int]:
        """
        Creates department using data from request from, returns dict containing message and status code
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
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
        except KeyError as error:
            return {'error': f'missing parameter {str(error)}'}, 400
        return {'success': 'department has been created'}, 201


class DepartmentAPI(Resource):
    """
    Resource class to work with single department
    """
    @staticmethod
    def get(department_id: UUID) -> Tuple[dict, int]:
        """
        Returns department with specified id
        :param department_id: id of a department
        :type department_id: UUID
        :return: tuple containing message dict or dict representation of a department and status code
        :rtype: Tuple[dict, int]
        """
        department = get_department_by_id(department_id)
        if not department:
            return {'error': 'Not Found'}, 404
        return department.to_dict(), 200

    @staticmethod
    def put(department_id: UUID) -> Tuple[dict, int]:
        """
        Updates department with specified id using data from request from,
        returns dict containing message and status code
        :param department_id: id of a department
        :type department_id: UUID
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
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

            is_updated = update_department(department_id, department_name, department_phone_number)
            if not is_updated:
                return {'error': 'Not Found'}, 404
        except KeyError as error:
            return {'error': f'missing parameter {str(error)}'}, 400
        return {'success': 'department has been updated'}, 201

    @staticmethod
    def delete(department_id: UUID):
        """
        Deletes department with specified id, returns dict containing message and status code
        :param department_id: id of a department
        :type department_id: UUID
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
        is_deleted = delete_department(department_id)
        if not is_deleted:
            return {'error': 'Not Found'}, 404
        return {'success': 'department has been deleted'}, 200
