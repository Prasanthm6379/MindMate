from flask import Blueprint



admin  = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/',methods=['GET','POST'])
def index():
    return 'Admin Home Page'