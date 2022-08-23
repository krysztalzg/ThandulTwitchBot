from os import path, makedirs
from json import dumps
from flask import Flask, render_template

from . import db
from .db import get_db

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def list():
        return render_template('index.html', items=['Coffee', 'Tea', 'Milk'])

    return app
