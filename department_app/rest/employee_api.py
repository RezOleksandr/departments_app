"""
Module containing REST API resource classes to work with employees
"""
from uuid import UUID
from datetime import datetime, date
from typing import Tuple, Union

from flask import request
from flask_restful import Resource
import validators

from department_app.service import get_all_employees, get_employees_with_filter, get_employee_by_id, \
    create_employee, delete_employee, update_employee, get_department_by_id


class EmployeesAPI(Resource):
    """
    Resource class to work with employees
    """
    @staticmethod
    def get() -> Tuple[Union[dict, list], int]:
        """
        Returns list of employees in the database that satisfy filtering options, received from request args
        or dict containing error message and status code
        :return: tuple containing list of departments or dict containing error message and status code
        :rtype: Tuple[Union[dict, list], int]
        """
        request_data = request.args.to_dict()

        if request_data:
            if 'department_id' in request_data:
                department_id = request_data['department_id']
                if not validators.uuid(department_id):
                    return {'error': 'department_id is invalid'}, 400
                department_id = UUID(department_id)
                if not get_department_by_id(department_id):
                    return {'error': 'department not found'}, 404
            else:
                department_id = None
            if 'start_date' in request_data:
                start_date = request_data['start_date']
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                except ValueError:
                    return {'error': 'start_date is invalid'}, 400
                else:
                    if not validators.between(start_date, max=date.today()):
                        return {'error': 'start_date is invalid'}, 400
            else:
                start_date = None
            if 'end_date' in request_data:
                end_date = request_data['end_date']
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                except ValueError:
                    return {'error': 'end_date is invalid'}, 400
                else:
                    if not validators.between(end_date, max=date.today()):
                        return {'error': 'end_date is invalid'}, 400
            else:
                end_date = None
            employees = get_employees_with_filter(department_id, start_date, end_date)
        else:
            employees = get_all_employees()
        employees_dicts = [employee.to_dict() for employee in employees]
        return employees_dicts, 200

    @staticmethod
    def post() -> Tuple[dict, int]:
        """
        Creates employee using data from request from, returns dict containing message and status code
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
        try:
            request_data = request.form.to_dict()
            employee_name = request_data['employee_name']
            if not validators.length(employee_name, min=2, max=32):
                return {'error': 'employee_name is invalid'}, 400

            position = request_data['position']
            if not validators.length(position, min=2, max=32):
                return {'error': 'position is invalid'}, 400

            salary = request_data['salary']
            try:
                salary = float(salary)
            except ValueError:
                return {'error': 'salary is invalid'}, 400
            else:
                if salary <= 0:
                    return {'error': 'salary is invalid'}, 400

            birthdate = request_data['birthdate']
            try:
                birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError:
                return {'error': 'birthdate is invalid'}, 400
            else:
                if not validators.between(birthdate, max=date.today()):
                    return {'error': 'birthdate is invalid'}, 400

            department_id = request_data['department_id']
            if not validators.uuid(department_id):
                return {'error': 'department_id is invalid'}, 400
            department_id = UUID(department_id)
            if not get_department_by_id(department_id):
                return {'error': 'department not found'}, 404

            create_employee(employee_name, position, salary, birthdate, department_id)
        except KeyError as error:
            return {'error': f'missing parameter {str(error)}'}, 400
        return {'success': 'employee has been created'}, 201


class EmployeeAPI(Resource):
    """
    Resource class to work with single employee
    """
    @staticmethod
    def get(employee_id: UUID) -> Tuple[dict, int]:
        """
        Returns employee with specified id
        :param employee_id: id of an employee
        :type employee_id: UUID
        :return: tuple containing message dict or dict representation of an employee and status code
        :rtype: Tuple[dict, int]
        """
        employee = get_employee_by_id(employee_id)
        if not employee:
            return {'error': 'Not Found'}, 404
        return employee.to_dict(), 200

    @staticmethod
    def put(employee_id: UUID):
        """
        Updates employee with specified id using data from request from,
        returns dict containing message and status code
        :param employee_id: id of a department
        :type employee_id: UUID
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
        try:
            request_data = request.form.to_dict()
            if 'employee_name' in request_data:
                employee_name = request_data['employee_name']
                if not validators.length(employee_name, min=2, max=32):
                    return {'error': 'employee_name is invalid'}, 400
            else:
                employee_name = None

            if 'position' in request_data:
                position = request_data['position']
                if not validators.length(position, min=2, max=32):
                    return {'error': 'position is invalid'}, 400
            else:
                position = None

            if 'salary' in request_data:
                salary = request_data['salary']
                try:
                    salary = float(salary)
                except ValueError:
                    return {'error': 'salary is invalid'}, 400
                else:
                    if salary <= 0:
                        return {'error': 'salary is invalid'}, 400
            else:
                salary = None

            if 'birthdate' in request_data:
                birthdate = request_data['birthdate']
                try:
                    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
                except ValueError:
                    return {'error': 'birthdate is invalid'}, 400
                else:
                    if not validators.between(birthdate, max=date.today()):
                        return {'error': 'birthdate is invalid'}, 400
            else:
                birthdate = None

            if 'department_id' in request_data:
                department_id = request_data['department_id']
                if not validators.uuid(department_id):
                    return {'error': 'department_id is invalid'}, 400
                department_id = UUID(department_id)
                if not get_department_by_id(department_id):
                    return {'error': 'department not found'}, 404
            else:
                department_id = None

            is_updated = update_employee(employee_id, employee_name, position, salary, birthdate, department_id)
            if not is_updated:
                return {'error': 'Not Found'}, 404
        except KeyError as error:
            return {'error': f'missing parameter {str(error)}'}, 400
        return {'success': 'employee has been updated'}, 201

    @staticmethod
    def delete(employee_id: UUID):
        """
        Deletes employee with specified id, returns dict containing message and status code
        :param employee_id: id of a department
        :type employee_id: UUID
        :return: tuple containing message dict and status code
        :rtype: Tuple[dict, int]
        """
        is_deleted = delete_employee(employee_id)
        if not is_deleted:
            return {'error': 'Not Found'}, 404
        return {'success': 'employee has been deleted'}, 200
