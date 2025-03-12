from datetime import datetime, timedelta
import smtplib
from flask_mail import  Message
import uuid
from helper import check_password, encrypt_password
from models import ActivityLog, EmergencyAlert, User, MemoryNote, Caregiver, Reminder
from config import db, s3_client, BUCKET, MAIL_PASSWORD, MAIL_USERNAME, MAIL_PORT, MAIL_SERVER
from werkzeug.exceptions import HTTPException
from botocore.exceptions import ClientError
import os
import sys
import threading


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
class DupicateResourceException(HTTPException):
    code = 409
    description = "Resource already exist"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)


class InvalidPasswordException(HTTPException):
    code = 401
    description = "Invalid password"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)


class UserNotFoundException(HTTPException):
    code = 404
    description = "User not found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)

class NoteNotFoundException(HTTPException):
    code = 404
    description = "Note not found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)


class InvalidUserIdException(HTTPException):
    code = 400
    description = "Invalid user id"
    def __init__(self, description = None, response = None):    
        if not description:
            description = self.description
        super().__init__(description, response)

class InvalidNoteTypeException(HTTPException):
    code = 400
    description = "Invalid note type (Should be from ['note','reminder','todo'])"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)
    

class CaregiverNotFoundException(HTTPException):
    code = 404
    description = "Caregiver not found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)

class RemainderNotFoundException(HTTPException):
    code = 404
    description = "Remainder Not Found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)

class EmergencyAlertNotFoundException(HTTPException):
    code = 404
    description = "Emergency Alert Not Found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)


class ActivityLogNotFoundException(HTTPException):
    code = 404
    description = "Activity Log Not Found"
    def __init__(self, description = None, response = None):
        if not description:
            description = self.description
        super().__init__(description, response)




def get_one_user_by_email(email):
    try:
        user = User.query.filter_by(email = email).first()
        if user:
            return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role, "is_active":user.is_active}}  
        else:
            raise UserNotFoundException()
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":404}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_one_user_by_username(username):
    try:
        user = User.query.filter_by(username = username).first()
        if user:
            return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role, "is_active":user.is_active}}  
        else:
            raise UserNotFoundException()
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":404}
    except Exception as e:
        return {"status":"failed","error":str(e)}

def get_hashed_password(email):
    password = User.query.filter_by(email=email).first().password
    return password

def create_user(email, username, password):
    try:
        password = encrypt_password(password)
        exist = get_one_user_by_email(email)
        print("test",exist)
        if exist['status'] == 'success':
            if exist['data']['is_active'] == True:
                raise DupicateResourceException()
            else:
                user = User.query.filter_by(email=email).first()
                user.email = email
                user.username = username
                user.is_active = True
                db.session.commit()
                return {"status":"success","data":"User registered successfully"}
        exist = get_one_user_by_username(username)
        if exist['status'] == 'success':
            if exist['data']['is_active']:
                raise DupicateResourceException()
            else:
                user = User.query.filter_by(username=username).first()
                user.email = email
                user.username = username
                user.is_active = True
                db.session.commit()
                return {"status":"success","data":"User registered successfully"}
        user = User(email=email, username = username,password=password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role}}
    except DupicateResourceException as e:
        return {"status":"failed to add user","error":str(e)}
    except Exception as e:
        return {"status":"failed to add user","error":str(e)}

def update_user(id,email,username,password):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            raise UserNotFoundException()
        user.email = email
        user.username = username
        user.password = encrypt_password(password)
        db.session.commit()
        return {"status":"success","data":"User updated successfully"}
    except UserNotFoundException as e:
        return {"status":"failed to update user","error":str(e),'status_code':e.code}
    except Exception as e:
        return {"status":"failed to update user","error":str(e)}


def delete_one_user(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            raise UserNotFoundException()
        if user.is_active == False:
            raise UserNotFoundException()
        user.is_active = False
        db.session.commit()
        return {"status":"success","data":"User deleted successfully"}
    except UserNotFoundException as e:
        return {"status":"failed to delete user","error":str(e),'status_code':e.code}
    except Exception as e:
        return {"status":"failed to delete user","error":str(e)}


def login(email,password):
    try:
        hash_password = get_hashed_password(email)
        password = password.encode('utf8')
        hash_password = hash_password.encode('utf8')
        if password and hash_password:
            if check_password(password = password, hash_password=hash_password):
                return {"status":"success","data":{"message":"User logged in successfully"}}
            raise InvalidPasswordException()
        raise UserNotFoundException()
    except InvalidPasswordException as e:
        return {"status":"failed to login","error":str(e),"status_code":e.code}
    except UserNotFoundException as e:
        return {"status":"failed to login","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed to login","error":str(e)}
    


def get_one_user_by_id(id):
    try:
        user = User.query.filter_by(id = id).first()
        if user:
            return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role}}  
        raise UserNotFoundException()
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":404}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def upload_file_s3(file_path):
    unique_id = uuid.uuid4().hex
    s3_object_name = f"uploads/{unique_id}_{file_path.split('/')[-1]}"
    s3_client.upload_file(file_path, BUCKET, s3_object_name,ExtraArgs={'ACL': 'public-read'},Callback=ProgressPercentage(file_path))
    return s3_object_name

def create_memory_note(id,note_type,content,title,file_path = None):
    try:
        user = get_one_user_by_id(id)
        if user['status'] == 'failed':
            raise InvalidUserIdException() 
        if note_type not in ['note','reminder','todo','img','video']:
            raise InvalidNoteTypeException()
        if note_type in ['img','video']:
            content = upload_file_s3(file_path)
        mem = MemoryNote(user_id=id,note_type=note_type,content=content,title=title)
        db.session.add(mem)
        db.session.commit()
        return {"status":"success","data":"Note created successfully"}
    except ClientError as e:
        return {"status":"failed","error":str(e)}
    except InvalidNoteTypeException as e:
        return {"status":"failed","error":str(e)}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e)}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def update_memory_note(id,user_id,note_type,content,title):
    try:
        user = get_one_user_by_id(user_id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        note = MemoryNote.query.filter_by(id=id,user_id=user_id).first()
        if not note:
            raise NoteNotFoundException()
        note.note_type = note_type
        note.content = content
        note.title = title
        db.session.commit()
        return {"status":"success","data":"Note updated successfully"}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"staus_code":e.code} 
    except NoteNotFoundException as e:
        return {"status":"failed","error":str(e), "status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}





def get_all_memory_notes(id):
    try:
        user = get_one_user_by_id(id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        notes = MemoryNote.query.filter_by(user_id=id).all()
        data = []
        for note in notes:
            if note.note_type in ['img','video']:
                data.append({"id":note.id,"title":note.title,"note_type":note.note_type,"content":f"https://{BUCKET}.s3.amazonaws.com/{note.content}","file_name":note.content.split('_')[-1]})
            else:
                data.append({"id":note.id,"title":note.title,"note_type":note.note_type,"content":note.content})
        return {"status":"success","data":data}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e)}
    except Exception as e:
        return {"status":"failed","error":str(e)} 



def get_one_memory_note_by_id(id,user_id):
    try:
        note = MemoryNote.query.filter_by(id=id,user_id=user_id).first()
        if note:
            data = {}
            if note.note_type in ['img','video']:
                data = {"id":note.id,"title":note.title,"note_type":note.note_type,"content":f"https://{BUCKET}.s3.amazonaws.com/{note.content}","file_name":note.content.split('_')[-1]}
            else:
                data = {"id":note.id,"title":note.title,"note_type":note.note_type,"content":note.content}
            return {"status":"success","data":data}  
        raise NoteNotFoundException()
    except NoteNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def delete_one_memory_note(id,user_id):
    try:
        note = MemoryNote.query.filter_by(id=id,user_id=user_id).first()
        if not note:
            raise NoteNotFoundException()
        db.session.delete(note)
        db.session.commit()
        return {"status":"success","data":"Note deleted successfully"}
    except NoteNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    


def add_caregiver(id,name,phone,email,relationship,emergency_contact):
    try:
        user = get_one_user_by_id(id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        caregiver = Caregiver(user_id=id,name = name,phone=phone,email=email,relationship=relationship,emergency_contact=emergency_contact)
        db.session.add(caregiver)
        db.session.commit()
        return {"status":"success","data":"Caregiver added successfully"}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_all_caregivers_by_id(id):
    try:
        user = get_one_user_by_id(id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        caregivers = Caregiver.query.filter_by(user_id=id).all()
        data = []
        for caregiver in caregivers:
            data.append({"id":caregiver.id,"name":caregiver.name,"phone":caregiver.phone,"email":caregiver.email,"relationship":caregiver.relationship,"emergency_contact":caregiver.emergency_contact})
        return {"status":"success","data":data}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def get_one_caregiver_by_id(id,user_id):
    try:
        user = get_one_user_by_id(user_id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        caregiver = Caregiver.query.filter_by(id=id,user_id=user_id).first()
        if caregiver:
            return {"status":"success","data":{ "id":caregiver.id,"name":caregiver.name, "phone":caregiver.phone,"email":caregiver.email,"relationship":caregiver.relationship,"emergency_contact":caregiver.emergency_contact}}
        raise CaregiverNotFoundException()
    except CaregiverNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def delete_one_caregiver(id,user_id):
    try:
        user = get_one_user_by_id(user_id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        caregiver = Caregiver.query.filter_by(id=id,user_id=user_id).first()
        if not caregiver:
            raise CaregiverNotFoundException()
        db.session.delete(caregiver)
        db.session.commit()
        return {"status":"success","data":"Caregiver deleted successfully"}
    except CaregiverNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def update_caregiver(id,user_id,name,phone,email,relationship,emergency_contact):
    try:
        user = get_one_user_by_id(user_id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        caregiver = Caregiver.query.filter_by(id=id,user_id=user_id).first()
        if not caregiver:
            raise CaregiverNotFoundException()
        caregiver.name = name
        caregiver.phone = phone
        caregiver.email = email
        caregiver.relationship = relationship
        caregiver.emergency_contact = emergency_contact
        db.session.commit()
        return {"status":"success","data":"Caregiver updated successfully"}
    except CaregiverNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def add_remainder(id,title,description,reminder_time,repeat_interval,reminder_type,status):
    try:
        user = get_one_user_by_id(id)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        remainder = Reminder(user_id=id,title = title,description=description,reminder_time=reminder_time,repeat_interval=repeat_interval,reminder_type=reminder_type,status=status)
        db.session.add(remainder)
        db.session.commit()
        return {"status":"success","data":"Remainder added successfully"}
    except InvalidUserIdException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_all_remainders():
    try:
        now = datetime.utcnow()
        rem = Reminder.query.filter(Reminder.reminder_time <= now, Reminder.status == False).all()
        data = []
        for reminder in rem:
            data.append({"id":reminder.id,"user_id":reminder.user_id,"title":reminder.title,"description":reminder.description,"reminder_time":reminder.reminder_time,"repeat_interval":reminder.repeat_interval,"reminder_type":reminder.reminder_type,"status":reminder.status})
        return {"status":"success","data":rem}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_all_remainders_by_id(id):
    try:
        remainders = Reminder.query.filter_by(user_id=id).all()
        data = []
        for rem in remainders:
            data.append({"id":rem.id,"user_id":rem.user_id,"title":rem.title,"description":rem.description,"reminder_time":rem.reminder_time,"repeat_interval":rem.repeat_interval,"reminder_type":rem.reminder_type,"status":rem.status})
        return {"status":"success","data":data}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_one_remainder(id):
    try:
        remainder = Reminder.query.filter_by(id=id).all()[0]
        if remainder:
            return {"status":"success","data":{"id":remainder.id,"user_id":remainder.user_id,"title":remainder.title,"description":remainder.description,"reminder_time":remainder.reminder_time,"repeat_interval":remainder.repeat_interval,"reminder_type":remainder.reminder_type,"status":remainder.status}}
        raise RemainderNotFoundException()
    except RemainderNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def edit_remainder(id,remainder_type,status,title,description,remainder_time,repeat_interval):
    try:
        remainder = Reminder.query.filter_by(id = id).all()
        if not remainder:
            raise RemainderNotFoundException()
        remainder = remainder[0]
        remainder.reminder_type = remainder_type
        remainder.status = status
        remainder.title = title
        remainder.description = description
        remainder.reminder_time = remainder_time
        remainder.repeat_interval = repeat_interval
        db.session.commit()
        print('remainder updated    ')
        return {"status":"success","data":"Remainder updated successfully"}
    except RemainderNotFoundException as e:
        return {"status":"failed","error":str(e),'status_code':e.code}
    except Exception as e:
        return {"status":"failed","error":str(e),'status_code':500}
        

def send_email_notification(user_email, title, description):
    try:        
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        message = f"Subject: Reminder - {title}\n\n{description}"
        server.sendmail(MAIL_USERNAME, user_email, message)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_remainder():
    now = datetime.utcnow()
    reminders = Reminder.query.filter(Reminder.reminder_time <= now, Reminder.status == False).all()
    for reminder in reminders:
        user = get_one_user_by_id(reminder.user_id)
        if not user:
            raise UserNotFoundException()
        user_email = user['data']['email']  
        send_email_notification(user_email=user_email, title=reminder.title, description=reminder.description)
        reminder.status = True
        db.session.commit()
        if reminder.repeat_interval:
            if reminder.repeat_interval == "daily":
                next_time = reminder.reminder_time + timedelta(days=1)
            elif reminder.repeat_interval == "weekly":
                next_time = reminder.reminder_time + timedelta(weeks=1)
            elif reminder.repeat_interval == "monthly":
                next_time = reminder.reminder_time + timedelta(weeks=4)
            else:
                next_time = None

            if next_time:
                new_reminder = Reminder(
                    user_id=reminder.user_id,
                    reminder_type=reminder.reminder_type,
                    status=False,
                    title=reminder.title,
                    description=reminder.description,
                    reminder_time=next_time,
                    repeat_interval=reminder.repeat_interval
                )
                db.session.add(new_reminder)
                db.session.commit()
    
    db.session.commit()
    return "Reminders checked and triggered."

def delete_one_remainder(id):
    try:
        remainder = Reminder.query.filter_by(id=id).first()
        if not remainder:
            raise RemainderNotFoundException()
        db.session.delete(remainder)
        db.session.commit()
        return {"status":"success","data":"Remainder deleted successfully"}
    except RemainderNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_all_EmergencyAlert_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            raise UserNotFoundException()
        alert = EmergencyAlert.query.filter_by(user_id=id).all()
        data = []
        for a in alert:
            data.append({"id":a.id,"user_id":a.user_id,"caregiver_id":a.caregiver_id,"alert_time":a.alert_time,"location":a.location,"resolved":a.resolved})
        return {"status":"success","data":data}
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def add_EmergencyAlert(id,caregiver_id,alert_time,location,resolved):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            raise UserNotFoundException()
        alert = EmergencyAlert(user_id=id,caregiver_id=caregiver_id,alert_time=alert_time,location=location,resolved=resolved)
        db.session.add(alert)
        db.session.commit()
        return {"status":"success","data":"Emergency Alert added successfully"}
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e),"status_code":500}


def get_one_EmergencyAlert(id):
    try:
        alert = EmergencyAlert.query.filter_by(id=id).first()
        if not alert:
            raise EmergencyAlertNotFoundException()
        return {"status":"success","data":{ "id":alert.id,"user_id":alert.user_id, "caregiver_id":alert.caregiver_id,"alert_time":alert.alert_time,"location":alert.location,"resolved":alert.resolved}}
    except EmergencyAlertNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e),"status_code":500}


def edit_EmergencyAlert(id,caregiver_id,alert_time,location,resolved):
    try:
        alert = EmergencyAlert.query.filter_by(id=id).first()
        if not alert:
            raise EmergencyAlertNotFoundException()
        alert.caregiver_id = caregiver_id
        alert.alert_time = alert_time
        alert.location = location
        alert.resolved = resolved
        db.session.commit()
        return {"status":"success","data":"Emergency Alert updated successfully"}
    except EmergencyAlertNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}
    

def delete_one_EmergencyAlert(id):
    try:
        alert = EmergencyAlert.query.filter_by(id=id).first()
        if not alert:
            raise EmergencyAlertNotFoundException()
        db.session.delete(alert)
        db.session.commit()
        return {"status":"success","data":"Emergency Alert deleted successfully"}
    except EmergencyAlertNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_all_ActivityLog_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            raise UserNotFoundException()
        activity = ActivityLog.query.filter_by(user_id=id).all()
        data = []
        for a in activity:
            data.append({"id":a.id,"user_id":a.user_id,"details":a.details,"activity_type":a.activity_type,"activity_time":a.activity_time})
        return {"status":"success","data":data}
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def add_ActivityLog(id,activity_type,details,activity_time):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            raise UserNotFoundException()
        activity = ActivityLog(user_id=id,activity_type=activity_type,details=details,activity_time=activity_time)
        db.session.add(activity)
        db.session.commit()
        return {"status":"success","data":"Activity Log added successfully"}
    except UserNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e),"status_code":500}


def edit_ActivityLog(id,activity_type,details,activity_time):
    try:
        activity = ActivityLog.query.filter_by(id=id).first()
        if not activity:
            raise ActivityLogNotFoundException()
        activity.activity_type = activity_type
        activity.details = details
        activity.activity_time = activity_time
        db.session.commit()
        return {"status":"success","data":"Activity Log updated successfully"}
    except ActivityLogNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def get_one_ActivityLog(id):
    try:
        activity = ActivityLog.query.filter_by(id=id).first()
        if not activity:
            raise ActivityLogNotFoundException()
        return {"status":"success","data":{ "id":activity.id,"user_id":activity.user_id, "details":activity.details,"activity_type":activity.activity_type,"activity_time":activity.activity_time}}
    except ActivityLogNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}


def delete_ActivityLog(id):
    try:
        activity = ActivityLog.query.filter_by(id=id).first()
        if not activity:
            raise ActivityLogNotFoundException()
        db.session.delete(activity)
        db.session.commit()
        return {"status":"success","data":"Activity Log deleted successfully"}
    except ActivityLogNotFoundException as e:
        return {"status":"failed","error":str(e),"status_code":e.code}
    except Exception as e:
        return {"status":"failed","error":str(e)}