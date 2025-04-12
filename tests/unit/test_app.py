# -*- coding: utf-8 -*-
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

# Fixture que configura o cliente de teste
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()

# Fixture que configura um usuário de teste
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

@pytest.mark.unit
def test_home_page(client):
    """Test home page"""
    response = client.get('/')
    assert response.status_code == 302

@pytest.mark.unit
def test_login(client, test_user):
    # Test login with correct credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Test login with incorrect credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert response.status_code == 200

@pytest.mark.unit
def test_register(client):
    # Test registration with valid data
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'securepass',
        'confirm_password': 'securepass'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Test registration with non-matching passwords
    response = client.post('/register', data={
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'pass1',
        'confirm_password': 'pass2'
    }, follow_redirects=True)
    assert response.status_code == 200

@pytest.mark.unit
def test_add_task(client, test_user):
    # Log in
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    # Test adding task
    response = client.post('/add_task', data={
        'title': 'Test Task',
        'description': 'This is a test task'
    }, follow_redirects=True)
    assert response.status_code == 200
