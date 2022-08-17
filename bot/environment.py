from os import getenv, environ
from ast import literal_eval
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
Environment = namedtuple(
    'Environment',
    [
        'prefix',
        'client_secret',
        'client_token',
        'channels',
    ]
)

bot_environment = Environment(
    environ.get('PREFIX', getenv('PREFIX')),
    environ.get('CLIENT_SECRET', getenv('CLIENT_SECRET')),
    environ.get('CLIENT_TOKEN', getenv('CLIENT_TOKEN')),
    literal_eval(environ.get('CHANNELS', getenv('CHANNELS'))),
)
