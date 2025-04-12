# tests/integration/test_views.py
import pytest
import os
import sys

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar do gerenciador centralizado de modelos
from models_manager import MainUser, MainTask, MainSystemLog, setup_test_db, cleanup_test_db
from db import db

# Importar a aplicação
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Extrair a aplicação do módulo importado
app = app_module.app

@pytest.fixture(scope="function")
def test_client():
    with app.test_client() as client:
        with app.app_context():
            # Usar as funções do models_manager para configuração limpa
            setup_test_db()
            yield client
            # Fechar todas as sessões e limpar o banco de dados
            db.session.close_all()
            cleanup_test_db()

def test_task_workflow(test_client):
    """Teste do fluxo completo de tarefas"""
    # Criar usuário
    with app.app_context():
        user = MainUser(username="workflow_user", email="workflow@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        # Garantir que o usuário esteja na sessão
        user = MainUser.query.filter_by(username="workflow_user").first()

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
        task = MainTask.query.filter_by(title="Integration Test Task").first()
        assert task is not None
        task_id = task.id

    # Marcar como concluída - usando POST já que a rota aceita apenas POST
    response = test_client.post(f"/toggle_task/{task_id}")
    assert response.status_code == 200

    # Verificar se foi marcada
    with app.app_context():
        task = MainTask.query.get(task_id)
        assert task.completed == True

    # Excluir tarefa - usando DELETE em vez de POST
    response = test_client.delete(f"/delete_task/{task_id}")
    assert response.status_code == 200

    # Verificar se a tarefa foi excluída
    with app.app_context():
        task = MainTask.query.get(task_id)
        assert task is None