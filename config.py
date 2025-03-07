import logging
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = f"{os.getenv('SQLALCHEMY_DATABASE_URI','postgresql://postgres:postgres@localhost:5432/mindmate')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True)

    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_TOKEN_TIME_OUT_IN_MINUTES', 25)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES', 60)))

    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DEBUG = os.getenv('DEBUG')
    LOG_OUTPUT = os.getenv('LOG_OUTPUT')
    LOAD_DOTENV = os.getenv('LOAD_DOTENV')
    USE_RELOADER = os.getenv('USE_RELOADER')
    ALLOW_UNSAFE_WERKZEUG = os.getenv('ALLOW_UNSAFE_WERKZEUG')


db = SQLAlchemy()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MindMate")
formatter = logging.Formatter('[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s',datefmt='%Y-%m-%d %I:%M:%S %p')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
