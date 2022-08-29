from os import path, makedirs
from json import dumps
from flask import Flask, render_template, redirect

from . import db
from .db import get_db

from sys import path as sys_path
sys_path.append('..')
from bot.environment import bot_environment

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=path.join(app.instance_path, 'database.sqlite'),
    )
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        try:
            db = get_db()
            tasks = db.execute(f'SELECT DISTINCT server FROM todo where done = FALSE').fetchall()
            return render_template('index.html', channels=[task['server'] for task in tasks])
        except:
            return render_error()

    @app.route("/<channel>")
    def list(channel):
        if channel is None:
            return render_error()

        try:
            db = get_db()
            tasks = db.execute(f'SELECT * FROM todo where server = "{channel.lower()}" AND done = FALSE').fetchall()
            return render_template('list.html', tasks=tasks)
        except:
            return render_error()

    @app.route("/test")
    def test():
        db = get_db()
        error = None

        try:
            db.execute(
                'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
                ('1', 'clarishy', 'test_user', '#000000', 'some task'),
            )
            db.commit()
            db.execute(
                'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
                ('2', 'clarishy', 'thandul', '#B35E19', 'finish the bot'),
            )
            db.commit()
            db.execute(
                'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
                ('3', 'clarishy', 'huntaa', '#FF0000', 'relacja z Pyrkonu'),
            )
            db.commit()
            db.execute(
                'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
                ('4', 'clarishy', 'test_user blue', '#0000FF', 'test task'),
            )
            db.commit()
        except db.IntegrityError:
            pass
        return redirect('/')

    def render_error():
        return 'Oops! Something went wrong.'

    return app
