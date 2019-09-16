from flask import Flask, jsonify
from flask_cors import CORS

from flask_jwt_extended import (JWTManager)

app = Flask(__name__)
CORS(app)

jwt = JWTManager(app)
from wordai.models import User



@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

from wordai.api.apis import blueprint as api

app.register_blueprint(api, url_prefix='/api')

