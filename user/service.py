from helper import check_password, encrypt_password
from models import User, MemoryNote, Caregiver
from config import db
from werkzeug.exceptions import HTTPException

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
            return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role}}  
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
            if exist['data']['is_active'] == True:
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
        return {"status":"success","data":"User registered successfully"}
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



def create_memory_note(id,note_type,content,title):
    try:
        user = get_one_user_by_id(id)
        print( user)
        if user['status'] == 'failed':
            raise InvalidUserIdException()
        
        if note_type not in ['note','reminder','todo']:
            raise InvalidNoteTypeException()
        
        mem = MemoryNote(user_id=id,note_type=note_type,content=content,title=title)
        db.session.add(mem)
        db.session.commit()
        return {"status":"success","data":"Note created successfully"}
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
            return {"status":"success","data":{ "id":note.id,"title":note.title, "note_type":note.note_type,"content":note.content}}  
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


def get_all_caregivers(id):
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


