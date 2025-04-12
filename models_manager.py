"""Gerenciador centralizado para modelos SQLAlchemy.

Este módulo fornece uma única instância compartilhada dos modelos
para evitar problemas de conflito quando importados em múltiplos arquivos.
"""

import os
import sys
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Garantir que o diretório raiz esteja no sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar a instância do SQLAlchemy
from db import db

# Definição dos modelos
class MainUser(db.Model, UserMixin):
    __tablename__ = "main_users"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('MainTask', backref='user', lazy=True, cascade="all, delete-orphan")
    system_logs = db.relationship('MainSystemLog', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MainTask(db.Model):
    __tablename__ = "main_tasks"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('main_users.id'), nullable=False)


class MainSystemLog(db.Model):
    __tablename__ = "main_system_logs"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('main_users.id'), nullable=False)
    
    def __init__(self, **kwargs):
        # Garantir que user_id seja fornecido
        if 'user_id' not in kwargs or kwargs['user_id'] is None:
            raise ValueError("user_id é obrigatório para criar um SystemLog")
        super().__init__(**kwargs)


# Funções auxiliares para testes
def setup_test_db():
    """Configura um banco de dados limpo para testes"""
    db.drop_all()
    db.create_all()

def create_test_user(username="testuser", email="testuser@example.com", password="testpass", is_admin=False):
    """Cria um usuário de teste e retorna a instância"""
    user = MainUser(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def create_test_task(user_id, title="Test Task", description="Test description"):
    """Cria uma tarefa de teste e retorna a instância"""
    task = MainTask(
        title=title,
        description=description,
        completed=False,
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return task

def create_test_log(user_id, action="Test action", details="Test details"):
    """Cria um log de sistema de teste e retorna a instância"""
    if user_id is None:
        raise ValueError("user_id não pode ser None ao criar um log do sistema")
        
    log = MainSystemLog(
        action=action,
        details=details,
        user_id=user_id
    )
    db.session.add(log)
    db.session.commit()
    return log

def cleanup_test_db():
    """Limpa o banco de dados de teste"""
    db.session.remove()
    db.drop_all()
