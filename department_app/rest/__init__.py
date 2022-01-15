from flask import Blueprint
from flask_restful import Api

rest_api = Blueprint('rest_api', __name__)
api = Api(rest_api)

from . import department_api
from . import employee_api
