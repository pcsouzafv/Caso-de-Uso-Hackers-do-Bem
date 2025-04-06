import os
import sys
import pytest
import tempfile

# Adiciona o diretório raiz ao PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_manager.app import app, db, User, Task


@pytest.fixture
def test_client():
    """Fixture para criar um cliente de teste"""
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE"]
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            # Criar usuário admin para testes
            admin = User(username="admin", is_admin=True)
            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()
        yield test_client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def test_login_page(test_client):
    """Teste da página de login"""
    rv = test_client.get("/")
    assert rv.status_code == 302  # Redireciona para login
    assert b"Redirecting" in rv.data


def test_login_success(test_client):
    """Teste de login bem-sucedido"""
    rv = test_client.post(
        "/login", data={"username": "admin", "password": "admin"}, follow_redirects=True
    )
    assert rv.status_code == 200
    assert b"Painel do Administrador" in rv.data


def test_login_failure(test_client):
    """Teste de login mal-sucedido"""
    rv = test_client.post(
        "/login", data={"username": "wrong", "password": "wrong"}, follow_redirects=True
    )
    assert b"Invalid username or password" in rv.data


def test_create_task(test_client):
    """Teste de criação de tarefa"""
    # Primeiro fazer login
    test_client.post("/login", data={"username": "admin", "password": "admin"})

    # Criar uma tarefa
    rv = test_client.post(
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
    with app.app_context():
        task = Task.query.filter_by(title="Test Task").first()
        assert task is not None
        assert task.description == "Test Description"


def test_toggle_task(test_client):
    """Teste de alternar estado da tarefa"""
    # Login
    test_client.post("/login", data={"username": "admin", "password": "admin"})

    # Criar uma tarefa primeiro
    test_client.post(
        "/add_task", data={"title": "Toggle Test", "description": "Test Description"}
    )

    # Pegar o ID da tarefa
    with app.app_context():
        task = Task.query.filter_by(title="Toggle Test").first()
        task_id = task.id

    # Alternar o estado da tarefa
    rv = test_client.post(f"/toggle_task/{task_id}")
    assert rv.status_code == 200

    # Verificar se o estado mudou
    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed == True
