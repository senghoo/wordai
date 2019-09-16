import os

def c(name, default=None):
    return os.environ.get(name.upper(), default)

def mongo_config():
    return {
        'host': c('mongo_host', "127.0.0.1"),
        'port': int(c('mongo_port', "27017")),
        'db': c('mongo_db', "wordai"),
        'username': c('mongo_username', "root"),
        'password': c('mongo_password', ""),
    }

def api_env():
    return {
        'host': c('host', '127.0.0.1'),
        'port': int(c('port', 8000)),
        'debug': c('debug', "true") == "true"
    }

def flask_config():
    return {
        'JWT_SECRET_KEY': c('secret', '__SOME_SECRET_KEYS_HERE__')
    }
