import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///task_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    TESTING = False
    LOGIN_DISABLED = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    DEBUG = False

class TestConfig(Config):
    TESTING = True
    LOGIN_DISABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True  # Para debug
    DEBUG = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False}
    }
