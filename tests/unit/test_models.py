import pytest
from task_manager.app import db, User, Task


def test_user_creation():
    """Teste de criação de usuário"""
    user = User(username="test_user")
    user.set_password("test123")

    assert user.username == "test_user"
    assert user.check_password("test123") == True
    assert user.check_password("wrong") == False
    assert user.is_admin == False


def test_admin_user_creation():
    """Teste de criação de usuário admin"""
    admin = User(username="admin_user", is_admin=True)
    admin.set_password("admin123")

    assert admin.username == "admin_user"
    assert admin.is_admin == True
    assert admin.check_password("admin123") == True


def test_task_creation():
    """Teste de criação de tarefa"""
    user = User(username="task_user")
    task = Task(title="Test Task", description="Test Description", user=user)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.user == user


def test_task_completion():
    """Teste de conclusão de tarefa"""
    task = Task(title="Complete Me")
    assert task.completed == False

    task.toggle()
    assert task.completed == True

    task.toggle()
    assert task.completed == False
