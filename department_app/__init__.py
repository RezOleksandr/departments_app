"""
A simple web application for managing departments and employees
"""

import os

from flask import Flask
from flask_uuid import FlaskUUID

from department_app import database
from department_app import models
from department_app import service
from department_app import rest
from department_app import views


def create_app(test_config: bool = False) -> Flask:
    """
    Initializes application, web service and database
    :param test_config: True to use testing configuration
    :type test_config: bool
    :return: returns Flask app
    :rtype: Flask
    """
    app = Flask(__name__, instance_relative_config=True)
    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile('test_config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    FlaskUUID(app)

    database.db.init_app(app)
    database.migrate.init_app(app, database.db)

    app.register_blueprint(rest.rest_api, url_prefix='/api')
    app.register_blueprint(views.departments)
    app.register_blueprint(views.employees)
    return app
