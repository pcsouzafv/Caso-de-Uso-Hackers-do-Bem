import pytest
from app.models import User, Task, SystemLog
from app import db

@pytest.mark.unit
def test_user_creation(test_app, test_user):
    """Test user creation"""
    assert test_user.username == 'testuser'
    assert test_user.email == 'testuser@example.com'
    assert test_user.check_password('testpass')
    assert not test_user.check_password('wrongpass')
    assert test_user.is_admin is False

@pytest.mark.unit
def test_user_password_hashing(test_app):
    """Test password hashing"""
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpass')
    
    assert user.password_hash is not None
    assert user.password_hash != 'testpass'
    assert user.check_password('testpass')
    assert not user.check_password('wrongpass')

@pytest.mark.unit
def test_task_creation(test_app, test_task):
    """Test task creation"""
    assert test_task.title == 'Test Task'
    assert test_task.description == 'Test description'
    assert test_task.completed is False
    assert test_task.user_id is not None
    assert test_task.created_at is not None

@pytest.mark.unit
def test_task_completion(test_app, test_task):
    """Test task completion status"""
    assert test_task.completed is False
    
    test_task.completed = True
    db.session.commit()
    
    assert test_task.completed is True

@pytest.mark.unit
def test_system_log_creation(test_app, test_system_log):
    """Test system log creation"""
    assert test_system_log.action == 'Test action'
    assert test_system_log.details == 'Test details'
    assert test_system_log.user_id is not None
    assert test_system_log.timestamp is not None

@pytest.mark.unit
def test_user_relationships(test_app, test_user, test_task, test_system_log):
    """Test user relationships with tasks and logs"""
    assert test_user.tasks[0].id == test_task.id
    assert test_user.logs[0].id == test_system_log.id
    assert len(test_user.tasks) == 1
    assert len(test_user.logs) == 1

@pytest.mark.unit
def test_task_relationships(test_app, test_task, test_user):
    """Test task relationships with user"""
    assert test_task.user.id == test_user.id
    assert test_task.user.username == 'testuser'

@pytest.mark.unit
def test_system_log_relationships(test_app, test_system_log, test_user):
    """Test system log relationships with user"""
    assert test_system_log.user.id == test_user.id
    assert test_system_log.user.username == 'testuser'
