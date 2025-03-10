from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from admin.views import admin
from user.views import user


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    JWTManager(app)
    CORS(app,origins = '*')
    return app