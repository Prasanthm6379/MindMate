from factory import create_app
from config import db, logger
from helper import encrypt_password
from models import User
from user.service import send_remainder
from flask_apscheduler import APScheduler

app = create_app()
scheduler = APScheduler()
db.init_app(app)
def check_and_trigger_reminders():
    with app.app_context():
        res = send_remainder()
    return res



def create_admin():
    if not User.query.filter_by(username='admin').first():
        user = User(username = 'admin', email = 'admin@gmail.com', password = encrypt_password('admin'), role = 'admin')
        db.session.add(user)
        db.session.commit()
        logger.info("Admin created successfully")


scheduler.add_job(id="reminder_task", func=check_and_trigger_reminders, trigger="interval", seconds=60)
scheduler.start()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()
        create_admin()
    app.run()