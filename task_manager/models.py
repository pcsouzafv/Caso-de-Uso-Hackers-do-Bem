from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.sql import func
from . import db

class TMUser(db.Model, UserMixin):
    __tablename__ = "tm_users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    tasks = db.relationship("TMTask", back_populates="user", cascade="all, delete-orphan")
    logs = db.relationship("TMSystemLog", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<TMUser {self.username}>"

class TMTask(db.Model):
    __tablename__ = "tm_tasks"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("tm_users.id"), nullable=False)
    user = db.relationship("TMUser", back_populates="tasks")

    def __repr__(self):
        return f"<TMTask {self.title}>"

class TMSystemLog(db.Model):
    __tablename__ = "tm_system_logs"

    id = db.Column(db.Integer, primary_key=True, index=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("tm_users.id"))
    user = db.relationship("TMUser", back_populates="logs")

    def __repr__(self):
        return f"<TMSystemLog {self.action}>"
