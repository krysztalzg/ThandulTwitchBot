from mimetypes import init
from pydoc import cli
from sqlite3 import connect, PARSE_DECLTYPES, Row
from click import command, echo
from flask import current_app, g
from os.path import dirname, abspath, join

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@command('init-db')
def init_db_command():
    init_db()
    echo('Database initialized.')

def get_db():
    if 'db' not in g:
        g.db = connect(
            current_app.config['DATABASE'],
            detect_types=PARSE_DECLTYPES
        )
        g.db.row_factory = Row
    return g.db

def get_db_detached():
    path = abspath(join(dirname(__file__), '..', 'instance', 'database.sqlite'))
    return connect(
            path,
            detect_types=PARSE_DECLTYPES
    )

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
