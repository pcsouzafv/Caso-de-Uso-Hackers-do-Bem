import pytest
from app import app, db
from models import User, Task, SystemLog

def test_user_model(test_app):
    with test_app.app_context():
        # Testar criação de usuário
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        # Verificar se o usuário foi criado
        assert User.query.count() == 1
        assert User.query.first().username == 'testuser'
        assert User.query.first().check_password('testpass')
        
        # Verificar se a senha não é armazenada em texto plano
        assert User.query.first().password_hash != 'testpass'

def test_task_model(test_app, test_user):
    with test_app.app_context():
        # Testar criação de tarefa
        task = Task(
            title='Test Task',
            description='This is a test task',
            user_id=test_user.id
        )
        db.session.add(task)
        db.session.commit()
        
        # Verificar se a tarefa foi criada
        assert Task.query.count() == 1
        assert Task.query.first().title == 'Test Task'
        assert Task.query.first().user_id == test_user.id

def test_system_log_model(test_app, test_user):
    with test_app.app_context():
        # Testar criação de log
        log = SystemLog(
            action='Test action',
            user_id=test_user.id
        )
        db.session.add(log)
        db.session.commit()
        
        # Verificar se o log foi criado
        assert SystemLog.query.count() == 1
        assert SystemLog.query.first().action == 'Test action'
        assert SystemLog.query.first().user_id == test_user.id
