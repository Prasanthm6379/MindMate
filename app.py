from factory import create_app
from config import db, logger
from helper import encrypt_password
from models import User


app = create_app()
db.init_app(app)


def create_admin():
    if not User.query.filter_by(username='admin').first():
        user = User(username = 'admin', email = 'admin@gmail.com', password = encrypt_password('admin'), role = 'admin')
        db.session.add(user)
        db.session.commit()
        logger.info("Admin created successfully")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()
        create_admin()
    logger.info("App is running")
    app.run()