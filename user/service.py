from helper import check_password, encrypt_password
from models import User
from config import db

def get_one_user_by_email(email):
    user = User.query.filter_by(email = email).first()
    return {"status":"success","data":{ "id":user.id,"email":user.email, "username":user.username,"role":user.role}} if user else {"status":"failed","data":"User not found"}



def get_hashed_password(email):
    password = User.query.filter_by(email=email).first().password
    return password

def create_user(email, username, password):
    try:
        password = encrypt_password(password)
        user = User(email=email, username = username,password=password)
        db.session.add(user)
        db.session.commit()
        return {"status":"success","data":"User registered successfully"}
    except Exception as e:
        return {"status":"failed to add user","error":str(e)}
    

def login(email,password):
    hash_password = get_hashed_password(email)
    password = password.encode('utf8')
    hash_password = hash_password.encode('utf8')
    if password and hash_password:
        if check_password(password = password, hash_password=hash_password):
            return {"status":"success","data":"User logged in successfully"}
        return {"status":"failed","data":"Invalid password"}
    return {"status":"failed","data":"User not found"}