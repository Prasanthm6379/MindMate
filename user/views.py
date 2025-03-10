from flask import Blueprint



user  = Blueprint('user', __name__, url_prefix='/user')


@user.route('/',methods=['GET','POST'])
def index():
    return 'User Home Page'