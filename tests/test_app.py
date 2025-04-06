import os
import sys
import pytest

# Configura o path do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task_manager import create_app
from task_manager.models import User, Task

@pytest.fixture
def app():
    """Cria uma instância do app para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        from task_manager.extensions import db
        db.create_all()
        
        # Cria usuário admin
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()

def test_login_page(client):
    """Teste da página de login"""
    rv = client.get("/")
    assert rv.status_code == 302  # Redireciona para login
    assert b"Redirecting" in rv.data


def test_login_success(client):
    """Teste de login bem-sucedido"""
    rv = client.post(
        "/login", data={"username": "admin", "password": "admin"}, follow_redirects=True
    )
    assert rv.status_code == 200
    assert b"Painel do Administrador" in rv.data


def test_login_failure(client):
    """Teste de login mal-sucedido"""
    rv = client.post(
        "/login", data={"username": "wrong", "password": "wrong"}, follow_redirects=True
    )
    assert b"Invalid username or password" in rv.data


def test_create_task(client):
    """Teste de criação de tarefa"""
    # Primeiro fazer login
    client.post("/login", data={"username": "admin", "password": "admin"})

    # Criar uma tarefa
    rv = client.post(
        "/add_task",
        data={
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2025-12-31",
        },
        follow_redirects=True,
    )

    assert rv.status_code == 200
    # Verificar se a tarefa foi criada
    with client.application.app_context():
        from task_manager.models import Task
        task = Task.query.filter_by(title="Test Task").first()
        assert task is not None
        assert task.description == "Test Description"


def test_toggle_task(client):
    """Teste de alternar estado da tarefa"""
    # Login
    client.post("/login", data={"username": "admin", "password": "admin"})

    # Criar uma tarefa primeiro
    client.post(
        "/add_task", data={"title": "Toggle Test", "description": "Test Description"}
    )

    # Pegar o ID da tarefa
    with client.application.app_context():
        from task_manager.models import Task
        task = Task.query.filter_by(title="Toggle Test").first()
        task_id = task.id

    # Alternar o estado da tarefa
    rv = client.post(f"/toggle_task/{task_id}")
    assert rv.status_code == 200

    # Verificar se o estado mudou
    with client.application.app_context():
        from task_manager.models import Task
        task = Task.query.get(task_id)
        assert task.completed == True
