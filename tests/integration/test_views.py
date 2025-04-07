# tests/integration/test_views.py
import pytest
from task_manager.models import User, Task

def test_task_workflow(test_client):
    """Teste do fluxo completo de tarefas"""
    # Criar usuário
    user = User(username="workflow_user")
    user.set_password("password123")
    with test_client.application.app_context():
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
    with test_client.application.app_context():
        task = Task.query.filter_by(title="Integration Test Task").first()
        assert task is not None
        task_id = task.id

    # Marcar como concluída
    response = test_client.post(f"/toggle_task/{task_id}")
    assert response.status_code == 200

    # Verificar se foi marcada
    with test_client.application.app_context():
        task = Task.query.get(task_id)
        assert task.completed == True

    # Excluir tarefa
    response = test_client.post(f"/delete_task/{task_id}")
    assert response.status_code == 200

    # Verificar se a tarefa foi excluída
    with test_client.application.app_context():
        task = Task.query.get(task_id)
        assert task is None