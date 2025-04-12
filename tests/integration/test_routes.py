import pytest
import os
import sys

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar diretamente do arquivo app.py e db.py
from db import db
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Extrair as classes e a aplicação do módulo importado
app = app_module.app
MainUser = app_module.MainUser
MainTask = app_module.MainTask
MainSystemLog = app_module.MainSystemLog

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()

@pytest.fixture
def test_user():
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        if not user:
            user = MainUser(username="testuser", email="testuser@example.com")
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()
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
    response = client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tarefas' in response.data

@pytest.mark.integration
def test_logout_route(client, test_user):
    """Test user logout"""
    # First login
    client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Now logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_add_task(client, test_user):
    """Test task addition"""
    # First login
    client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Add task
    response = client.post('/add_task', data={
        'title': 'New Task',
        'description': 'Task description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Task' in response.data

@pytest.mark.integration
def test_admin_dashboard(client, test_user):
    """Test admin dashboard"""
    # First login
    client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Temporarily make user admin
    with app.app_context():
        user = MainUser.query.filter_by(username='testuser').first()
        user.is_admin = True
        db.session.commit()
        
        # Ensure user is in session
        db.session.refresh(user)
    
    # Test admin dashboard
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
