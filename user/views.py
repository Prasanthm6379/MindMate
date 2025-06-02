from flask import Blueprint, request
from user.service import (add_remainder, create_user, delete_one_caregiver, delete_one_remainder, delete_one_user, edit_remainder, 
                          get_all_caregivers_by_id, get_all_remainders_by_id, get_one_caregiver_by_id, get_one_remainder, 
                          get_one_user_by_email, login, create_memory_note, get_all_memory_notes, get_one_memory_note_by_id, delete_one_memory_note,
                            add_caregiver, update_caregiver, update_memory_note, update_user, get_all_EmergencyAlert_by_id, get_one_EmergencyAlert,
                              delete_one_EmergencyAlert, add_EmergencyAlert, edit_EmergencyAlert,edit_ActivityLog,get_all_ActivityLog_by_id, add_ActivityLog,
                              delete_ActivityLog,get_one_ActivityLog)
from helper import success_response,failure_response, tokengen
from flask_jwt_extended import jwt_required
from config import logger

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
                logger.info("User registered Successfully")
                return success_response(data=user['data'])
            logger.error(user['error'])
            return failure_response(data=user['error'])
        except Exception as e:
            logger.error(str(e))
            return failure_response(data=str(e),status_code=500)
        

@user.route('/',methods=['PUT'])
@jwt_required()
def update_one_user():
    try:
        payload = request.get_json()
        user = update_user(email = payload.get('email').lower(),username = payload.get('username'),password = payload.get('password'),id = payload.get('id'))
        if user['status'] == 'success':
            logger.info(user['data'])
            return success_response(data=user['data'])
        logger.error(user['error'])
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        logger.error(str(e))
        return failure_response(data=str(e),status_code=500)


@user.route('/<email>',methods=['DELETE'])
@jwt_required()
def delete_user(email):
    try:
        user = delete_one_user(email)
        if user['status'] == 'success':
            logger.info(user['data'])
            return success_response(data=user['data'])
        logger.error(user['error'])
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        logger.error(str(e))
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
            logger.info(user['data']['message'])
            return success_response(data={"message":user['data'],"token":token_})
        logger.error(user['error'])
        return failure_response(data=user['error'],status_code=user['status_code'])
    except Exception as e:
        logger.error(str(e))
        return failure_response(data=str(e),status_code=500)
    


@user.route('/memoryNote/<id>',methods=['POST','GET','PUT'])
@jwt_required()
def memory_note(id):
    if request.method == 'GET':
        print(id)
        note = get_all_memory_notes(id)
        if note['status'] == 'success':
            logger.info("Notes retrived Successfully")
            print(note['data'])
            return note['data']
        logger.error(note['error'])
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
                logger.info('Note created successfully')
                return success_response(data="Note created successfully")
            logger.error(note['error'])
            return failure_response(data = note['error'],status_code=400)
        except Exception as e:
            logger.error(str(e))
            return failure_response(data=str(e),status_code=500)
    elif request.method == 'PUT':
        try:
            payload = request.get_json()
            note = update_memory_note(user_id = payload.get('user_id'),id = payload.get('id'),title = payload.get('title'),note_type = payload.get('note_type'),content = payload.get('content'))
            if note['status'] == 'success':
                logger.info(note['data'])
                return success_response(data=note['data'])
            logger.error(note['error'])
            return failure_response(data=note['error'],status_code=note['status_code'])
        except Exception as e:
            logger.error(str(e))
            return failure_response(data = str(e),status_code=500)

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



@user.route('/caregiver/<user_id>',methods=['POST','GET','PUT'])
@jwt_required()
def caregiver(user_id):
    if request.method == 'GET':
        # id = request.get_json().get('id')
        data = get_all_caregivers_by_id(user_id)
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
        care = add_caregiver(id = payload.get('user_id'),name = payload.get('name'),phone = payload.get('phone'),email = payload.get('email'),relationship = payload.get('relationship'),emergency_contact = payload.get('emergency_contact'))
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


@user.route('/remainder/<user_id>',methods = ['POST','GET','PUT','DELETE'])
@jwt_required()
def remainder(user_id):
    try:
        if request.method == 'POST':
            payload = request.get_json()
            rem = add_remainder(id = payload.get('user_id'),title = payload.get('title'),description = payload.get('description'),reminder_time = payload.get('reminder_time'),repeat_interval = payload.get('repeat_interval'),reminder_type = payload.get('reminder_type'),status = payload.get('status'))
            if rem['status'] == 'success':
                logger.info(rem['data'])
                print(rem['data'])
                return rem['data']
            logger.error(rem['error'])
            return failure_response(data=rem['error'],status_code=rem['status_code'])
        elif request.method == 'GET':
            # user_id = request.get_json().get('user_id')
            remainders = get_all_remainders_by_id(user_id)
            if remainders['status'] == 'success':
                logger.info("Remainders retrived successfully")
                print(remainders.get("data"))
                return remainders.get('data')
            logger.error(remainders['error'])
            return failure_response(data=remainders['error'],status_code=remainders['status_code'])
        elif request.method == 'PUT':
            payload = request.get_json()
            rem = edit_remainder(id = payload.get('remainder_id'),title = payload.get('title'),description = payload.get('description'),remainder_time = payload.get('reminder_time'),repeat_interval = payload.get('repeat_interval'),remainder_type = payload.get('reminder_type'),status = payload.get('status'))
            if rem['status'] == 'success':
                return success_response(data=rem['data'])
            return failure_response(data=rem['error'],status_code=rem['status_code'])
        elif request.method == 'DELETE':
            remainder_id = request.get_json().get('remainder_id')
            rem = delete_one_remainder(remainder_id)
            if rem['status'] == 'success':
                return success_response(data=rem['data'])
            return failure_response(data=rem['error'],status_code=rem['status_code'])
    except Exception as e:
        logger.error(str(e))
        return failure_response(data=str(e),status_code=500)


@user.route('/remainder/<id>',methods=['GET'])
@jwt_required()
def one_remainder(id):
    try:
        remainder = get_one_remainder(id)
        if remainder['status'] == 'success':
            return success_response(data=remainder['data'])
        return failure_response(data=remainder['error'],status_code=remainder['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)


@user.route('/emergencyalert/<user_id>',methods=['POST','GET','PUT','DELETE'])
@jwt_required()
def emegencyAlert(user_id):
    try:
        if request.method == 'GET':
            # user_id = request.get_json().get('user_id')
            alerts = get_all_EmergencyAlert_by_id(user_id)
            if alerts['status'] == 'success':
                return success_response(data=alerts['data'])
            return failure_response(data=alerts['error'],status_code=alerts['status_code'])
        elif request.method == 'POST':
            payload = request.get_json()
            alert = add_EmergencyAlert(id = payload.get('user_id'),caregiver_id = payload.get('caregiver_id'),alert_time = payload.get('alert_time'),location = payload.get('location'),resolved = payload.get('resolved'))
            if alert['status'] == 'success':
                return success_response(data=alert['data'])
            return failure_response(data=alert['error'],status_code=alert['status_code'])
        elif request.method == 'PUT':
            payload = request.get_json()
            alert = edit_EmergencyAlert(id = payload.get('id'),caregiver_id = payload.get('caregiver_id'),alert_time = payload.get('alert_time'),location = payload.get('location'),resolved = payload.get('resolved'))
            if alert['status'] == 'success':
                return success_response(data=alert['data'])
            return failure_response(data=alert['error'],status_code=alert['status_code'])
        elif request.method == 'DELETE':
            payload = request.get_json()
            alert = delete_one_EmergencyAlert(id = payload.get('id'))
            if alert['status'] == 'success':
                return success_response(data=alert['data'])
            return failure_response(data=alert['error'],status_code=alert['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)

@user.route('/emergencyalert/<id>',methods=['GET'])
@jwt_required()
def one_emergency_alert(id):
    try:
        alert = get_one_EmergencyAlert(id = id)
        if alert['status'] == 'success':
            return success_response(data=alert['data'])
        return failure_response(data=alert['error'],status_code=alert['status_code'])
    except Exception as e:
        return failure_response(data=str(e),status_code=500)

@user.route('/activitylog/<user_id>',methods=['POST','GET','PUT','DELETE'])
@jwt_required() 
def activity(user_id):
    try:
        if request.method == 'GET':
            # user_id = request.get_json().get('user_id')
            logs = get_all_ActivityLog_by_id(user_id)
            if logs['status'] == 'success':
                return success_response(data=logs['data'])
            return failure_response(data=logs['error'],status_code=logs['status_code'])
        elif request.method == 'POST':
            payload = request.get_json()
            log = add_ActivityLog(id = payload.get('user_id'),activity_type = payload.get('activity_type'),activity_time = payload.get('activity_time'),details = payload.get('details'))
            if log['status'] == 'success':
                return success_response(data=log['data'])
            return failure_response(data=log['error'],status_code=log['status_code'])
        elif request.method == 'PUT':
            payload = request.get_json()
            log = edit_ActivityLog(id = payload.get('id'),activity_type = payload.get('activity_type'),activity_time = payload.get('activity_time'),details = payload.get('details'))
            if log['status'] == 'success':
                return success_response(data=log['data'])
            return failure_response(data=log['error'],status_code=log['status_code'])
        elif request.method == 'DELETE':
            payload = request.get_json()
            log = delete_ActivityLog(id = payload.get('id'))
            if log['status'] == 'success':
                return success_response(data=log['data'])
            return failure_response(data=log['error'],status_code=log['status_code'])
    except Exception as e:
        # print(request.get_json())
        logger.error(str(e))
        return failure_response(data=str(e),status_code=500)


# @user.route('/activitylog/<id>',methods=['GET'])
# @jwt_required()
# def one_activity_log(id):
#     try:
#         log = get_one_ActivityLog(id = id)
#         if log['status'] == 'success':
#             return success_response(data=log['data'])
#         return failure_response(data=log['error'],status_code=log['status_code'])
#     except Exception as e:
#         return failure_response(data=str(e),status_code=500)