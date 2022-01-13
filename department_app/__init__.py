import os
import department_app.database as database
import department_app.models as models

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.db.init_app(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
