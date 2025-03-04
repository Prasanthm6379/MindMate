from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app)
    CORS(app,origins = '*')
    return app