from flask import Blueprint, request
from user.service import create_user, get_one_user_by_email, login
from helper import success_response,failure_response, tokengen
from flask_jwt_extended import jwt_required


user  = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<email>',methods=['GET'])
@jwt_required()
def get_one_user(email):
    user = get_one_user_by_email(email)
    if user['status'] == 'success':
        return success_response(data=user['data'])
    return failure_response(data=user['data'],status_code=404)



@user.route('/register',methods=['POST'])
def register_user():
    try:
        payload = request.get_json()
        email = payload.get('email').lower()
        username = payload.get('username')
        password = payload.get('password')
        user = create_user(email,username,password)
        if user['status'] == 'success':
            return success_response(data=user['data'])
        return failure_response(data=user['error'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)
    


@user.route('/login',methods=['POST'])
def login_user():
    try:
        payload = request.get_json()
        email = payload.get('email').lower()
        password = payload.get('password')
        user = get_one_user_by_email(email)
        if user['status'] == 'success':
            log = login(email,password)
            if log['status'] == 'success':
                token_ = tokengen(user['data']['username'])
                return success_response(data={"message":log['data'],"token":token_})
            return failure_response(data=log['data'],status_code=401)
        return failure_response(data=user['data'],status_code=404)
    except Exception as e:
        return failure_response(data=str(e),status_code=500)