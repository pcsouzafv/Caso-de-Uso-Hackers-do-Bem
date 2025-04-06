# tests/unit/test_models.py
import pytest
from task_manager.models import User, Task

def test_password_hashing(app):
    """Testa o hash de senha"""
    with app.app_context():
        user = User(username='test')
        user.set_password('password')
        assert user.check_password('password')
        assert not user.check_password('wrong')

def test_task_creation(app):
    """Testa criação de tarefa"""
    with app.app_context():
        user = User(username='test')
        db.session.add(user)
        db.session.commit()
        
        task = Task(title='Test Task', description='Test', user_id=user.id)
        db.session.add(task)
        db.session.commit()
        
        assert task.id is not None