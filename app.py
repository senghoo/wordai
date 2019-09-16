from wordai.api import app
from config import api_env, flask_config

app.config.update(flask_config())

def run_dev():
    app.run(**api_env())
