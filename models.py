from config import db
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from uuid import uuid4

def default_uuid():
    return uuid4().hex  

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(40), default='user')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    caregivers = db.relationship('Caregiver', back_populates='user', cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', back_populates='user', cascade="all, delete-orphan")
    emergency_alerts = db.relationship('EmergencyAlert', back_populates='user', cascade="all, delete-orphan")
    memory_notes = db.relationship('MemoryNote', back_populates='user', cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', back_populates='user', cascade="all, delete-orphan")

class Caregiver(db.Model):
    __tablename__ = 'caregivers'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    relationship = db.Column(db.String(50))  
    emergency_alerts = db.relationship('EmergencyAlert', back_populates='caregiver')
    emergency_contact = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='caregivers')  

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    reminder_time = db.Column(db.DateTime, nullable=False)
    repeat_interval = db.Column(db.String(50)) 
    reminder_type = db.Column(db.String(50))  
    status = db.Column(db.Boolean, default=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reminders')

class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alerts'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    caregiver_id = db.Column(db.String(40), db.ForeignKey('caregivers.id'), nullable=True)
    alert_time = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.Text)  
    resolved = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='emergency_alerts')
    caregiver = db.relationship('Caregiver', back_populates='emergency_alerts')  


class MemoryNote(db.Model):
    __tablename__ = 'memory_notes'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255))
    note_type = db.Column(db.String(50)) 
    content = db.Column(db.Text) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='memory_notes')

class ActivityLog(db.Model):
    __tablename__ = 'activity_log'

    id = db.Column(db.String(40), primary_key=True, default=default_uuid)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50)) 
    details = db.Column(db.Text)
    activity_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='activity_logs')