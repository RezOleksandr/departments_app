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


def create_app():
    """
    Initializes application, web service and database
    :return:
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
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
