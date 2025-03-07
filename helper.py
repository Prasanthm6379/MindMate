import bcrypt


def encrypt_password(password=None):
    hash_password = bcrypt.hashpw(password=password.encode('utf8'), salt=bcrypt.gensalt())
    return hash_password.decode('utf8')


def check_password(password=None, hash_password=None):
    return bcrypt.checkpw(password=password, hashed_password=hash_password)