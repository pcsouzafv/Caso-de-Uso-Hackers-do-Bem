import pytest
from app import db
from models import User, Task


class TestUserModel:
    def test_password_hashing(self, app):
        u = User(username='testuser')
        u.set_password('cat')
        assert u.check_password('cat') is True
        assert u.check_password('dog') is False


class TestTaskModel:
    def test_task_creation(self, app):
        t = Task(title='Test Task', description='Test Description')
        assert t.title == 'Test Task'
        assert t.completed is False
