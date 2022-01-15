import os

from flask import Flask
from flask_uuid import FlaskUUID

import department_app.database as database
import department_app.models as models
import department_app.service as service
import department_app.rest as rest


def create_app():
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
    return app
