import pytest
from app import app, db, User, Task


@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
        db.session.remove()
        db.drop_all()


def test_task_workflow(test_client):
    """Teste do fluxo completo de tarefas"""
    # Criar usuário
    user = User(username="workflow_user")
    user.set_password("password123")
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Login
    response = test_client.post(
        "/login",
        data={"username": "workflow_user", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Criar tarefa
    response = test_client.post(
        "/add_task",
        data={
            "title": "Integration Test Task",
            "description": "Testing the full workflow",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Verificar se a tarefa foi criada
    with app.app_context():
        task = Task.query.filter_by(title="Integration Test Task").first()
        assert task is not None
        task_id = task.id

    # Marcar como concluída
    response = test_client.post(f"/toggle_task/{task_id}")
    assert response.status_code == 200

    # Verificar se foi marcada
    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed == True

    # Excluir tarefa
    response = test_client.post(f"/delete_task/{task_id}")
    assert response.status_code == 200

    # Verificar se foi excluída
    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None


def test_admin_user_management(test_client):
    """Teste do gerenciamento de usuários pelo admin"""
    # Criar admin
    admin = User(username="admin_test", is_admin=True)
    admin.set_password("admin123")
    with app.app_context():
        db.session.add(admin)
        db.session.commit()

    # Login como admin
    response = test_client.post(
        "/login",
        data={"username": "admin_test", "password": "admin123"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Criar novo usuário
    response = test_client.post(
        "/add_user",
        data={"username": "new_user", "password": "user123", "is_admin": False},
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Verificar se o usuário foi criado
    with app.app_context():
        user = User.query.filter_by(username="new_user").first()
        assert user is not None
        assert user.is_admin == False
        user_id = user.id

    # Excluir usuário
    response = test_client.post(f"/delete_user/{user_id}")
    assert response.status_code == 200

    # Verificar se foi excluído
    with app.app_context():
        user = User.query.get(user_id)
        assert user is None
