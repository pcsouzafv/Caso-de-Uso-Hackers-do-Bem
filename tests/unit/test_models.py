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

@pytest.mark.unit
def test_task_creation(test_app, test_task):
    """Test task creation"""
    assert test_task.title == 'Test Task'
    assert test_task.description == 'Test description'
    assert test_task.completed is False
    assert test_task.user_id is not None

@pytest.mark.unit
def test_system_log_creation(test_app, test_system_log):
    """Test system log creation"""
    assert test_system_log.action == 'Test action'
    assert test_system_log.user_id is not None
    assert test_system_log.timestamp is not None
