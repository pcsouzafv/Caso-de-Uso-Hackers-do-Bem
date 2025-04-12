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

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            setup_test_db()
            yield client
            cleanup_test_db()

@pytest.fixture
def test_user():
    with app.app_context():
        # Verificar se o usuário já existe
        user = MainUser.query.filter_by(username="testuser").first()
        if not user:
            user = MainUser(username="testuser", email="testuser@example.com")
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()
            # Recarregar o usuário da sessão após o commit
            user = MainUser.query.filter_by(username="testuser").first()
        
        # Garantir que o teste retorne uma instância vinculada à sessão atual
        db.session.refresh(user)
        return user

@pytest.mark.integration
def test_login_route(client):
    """Test login route"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_login_user(client, test_user):
    """Test user login"""
    # Garantir que o usuário esteja na sessão atual
    with app.app_context():
        db.session.refresh(test_user)
        
        response = client.post('/login', data={
            'username': test_user.username,
            'password': 'testpass'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Tarefas' in response.data or b'Task' in response.data

@pytest.mark.integration
def test_logout_route(client, test_user):
    """Test user logout"""
    # Garantir que o usuário esteja na sessão atual
    with app.app_context():
        db.session.refresh(test_user)
        
        # Primeiro login
        client.post('/login', data={
            'username': test_user.username,
            'password': 'testpass'
        }, follow_redirects=True)
        
        # Agora logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data

@pytest.mark.integration
def test_add_task(client, test_user):
    """Test task addition"""
    # Garantir que o usuário esteja na sessão atual
    with app.app_context():
        db.session.refresh(test_user)
        
        # Primeiro login
        client.post('/login', data={
            'username': test_user.username,
            'password': 'testpass'
        }, follow_redirects=True)
        
        # Adicionar tarefa
        response = client.post('/add_task', data={
            'title': 'New Task',
            'description': 'Task description'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'New Task' in response.data

@pytest.mark.integration
def test_admin_dashboard(client, test_user):
    """Test admin dashboard"""
    # Garantir que o usuário esteja na sessão atual e defini-lo como admin
    with app.app_context():
        db.session.refresh(test_user)
        test_user.is_admin = True
        db.session.commit()
        db.session.refresh(test_user)  # Recarregar após a alteração
        
        # Primeiro login
        client.post('/login', data={
            'username': test_user.username,
            'password': 'testpass'
        }, follow_redirects=True)
        
        # Testar dashboard admin
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data
