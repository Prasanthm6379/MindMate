from config import db
from datetime import datetime, timezone
from uuid import uuid4


def default_uuid():
    return uuid4().hex

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.String(40), primary_key=True, default=lambda: default_uuid())
    created_by = db.Column(db.String(40))
    updated_by = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))


class User(Base):
    __tablename__ = 'users'
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(40), default='user')