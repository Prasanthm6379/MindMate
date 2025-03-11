from flask import Blueprint, request
from user.service import create_user, delete_one_caregiver, delete_one_user, get_all_caregivers_by_id, get_one_caregiver_by_id, get_one_user_by_email, login, create_memory_note, get_all_memory_notes, get_one_memory_note_by_id, delete_one_memory_note, add_caregiver, update_caregiver, update_memory_note, update_user
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



@user.route('/',methods=['POST'])
def register_user():
    if request.method == 'POST':
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
        

@user.route('/',methods=['PUT'])
@jwt_required()
def update_one_user():
    try:
        payload = request.get_json()
        user = update_user(email = payload.get('email').lower(),username = payload.get('username'),password = payload.get('password'),id = payload.get('id'))
        if user['status'] == 'success':
            return success_response(data=user['data'])
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)


@user.route('/<email>',methods=['DELETE'])
@jwt_required()
def delete_user(email):
    try:
        user = delete_one_user(email)
        if user['status'] == 'success':
            return success_response(data=user['data'])
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)
    

@user.route('/login',methods=['POST'])
def login_user():
    try:
        payload = request.get_json()
        email = payload.get('email').lower()
        password = payload.get('password')
        user = login(email,password)
        if user['status'] == 'success':
            token_ = tokengen(email)
            # print(token_)
            return success_response(data={"message":user['data'],"token":token_})
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)
    


@user.route('/memoryNote/<id>',methods=['POST','GET','PUT'])
@jwt_required()
def memory_note(id):
    if request.method == 'GET':
        note = get_all_memory_notes(id)
        if note['status'] == 'success':
            return success_response(data=note['data'])
        return failure_response(data=note['error'],status_code=404)
    elif request.method == 'POST':
        try:
            # payload = request.form()
            title = request.form['title']
            note_type = request.form['note_type']
            if note_type in ['img','video']:
                content = request.files['content']
                file_path = f'uploads/{content.filename}'
                content.save(file_path)
                note = create_memory_note(id,note_type,content,title,file_path = file_path)
            else:
                content = request.form['content']
                note = create_memory_note(id,note_type,content,title)
            if note['status'] == 'success':
                return success_response(data="Note created successfully")
            return failure_response(data = note['error'],status_code=400)
        except Exception as e:
            return failure_response(data=str(e),status_code=500)
    elif request.method == 'PUT':
        payload = request.get_json()
        note = update_memory_note(user_id = payload.get('user_id'),id = payload.get('id'),title = payload.get('title'),note_type = payload.get('note_type'),content = payload.get('content'))
        if note['status'] == 'success':
            return success_response(data=note['data'])
        return failure_response(data=note['error'],status_code=note['status_code'])


@user.route('/memoryNote/<user_id>/<id>',methods=['GET', 'DELETE'])
@jwt_required()
def get_memory_note_by_id(user_id,id):
    if request.method == 'GET':
        try:
            note = get_one_memory_note_by_id(user_id = user_id,id =id)
            if note['status'] == 'success':
                return success_response(data=note['data'])
            return failure_response(data=note['error'],status_code=note['status_code'])
        except Exception as e:
            return failure_response(data=str(e),status_code=500)
    elif request.method == 'DELETE':
        try:
            note = delete_one_memory_note(user_id = user_id,id =id)
            if note['status'] == 'success':
                return success_response(data=note['data'])
            return failure_response(data=note['error'],status_code=note['status_code'])
        except Exception as e:
            return failure_response(data=str(e),status_code=500)



@user.route('/caregiver',methods=['POST','GET','PUT'])
@jwt_required()
def caregiver():
    if request.method == 'GET':
        id = request.get_json().get('id')
        data = get_all_caregivers_by_id(id)
        if data['status'] == 'failed':
            return failure_response(data=data['error'],status_code=data['status_code'])
        return success_response(data=data['data'])
    elif request.method == 'PUT':
        payload = request.get_json()
        caregiver = update_caregiver(user_id = payload.get('user_id'),id = payload.get('id'),name = payload.get('name'),phone = payload.get('phone'),email = payload.get('email'),relationship = payload.get('relationship'),emergency_contact = payload.get('emergency_contact'))
        if caregiver['status'] == 'success':
            return success_response(data=caregiver['data'])
        return failure_response(data=caregiver['error'],status_code=caregiver['status_code'])
    elif request.method == 'POST':
        payload = request.get_json()
        care = add_caregiver(id = payload.get('id'),name = payload.get('name'),phone = payload.get('phone'),email = payload.get('email'),relationship = payload.get('relationship'),emergency_contact = payload.get('emergency_contact'))
        if care['status'] == 'failed':
            return failure_response(data=care['error'],status_code=care['status_code'])
        return success_response(data=care['data'])


@user.route('/caregiver/<user_id>/<id>',methods=['GET','DELETE'])
@jwt_required()
def one_caregiver(user_id,id):
    if request.method == 'GET':
        caregiver = get_one_caregiver_by_id(user_id = user_id,id = id)
        if caregiver['status'] == 'success':
            return success_response(data=caregiver['data'])
        return failure_response(data=caregiver['error'],status_code=caregiver['status_code'])

    elif request.method == 'DELETE':
        caregiver = delete_one_caregiver(user_id = user_id,id = id)
        if caregiver['status'] == 'success':
            return success_response(data=caregiver['data'])
        return failure_response(data=caregiver['error'],status_code=caregiver['status_code'])

