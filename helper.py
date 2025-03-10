import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token


def encrypt_password(password=None):
    hash_password = bcrypt.hashpw(password=password.encode('utf8'), salt=bcrypt.gensalt())
    return hash_password.decode('utf8')


def check_password(password=None, hash_password=None):
    return bcrypt.checkpw(password=password, hashed_password=hash_password)


def success_response(data=None,status_code=200) -> list:
    return jsonify({"status": "success", "data": data, "status_code": status_code}),status_code


def failure_response(data=None, status_code=400):
    return jsonify({"status": "failed", "data": data, "status_code": status_code}), status_code


def tokengen(email):
    try:
        token_ = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return {"token": token_, "refresh_token": refresh_token}
    except Exception as e:
        return failure_response(401, "Unauthorized")