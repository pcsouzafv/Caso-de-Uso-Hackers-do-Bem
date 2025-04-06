import pytest
from app import app, db
from models import User, Task

def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_user(client, test_user):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tarefas' in response.data

def test_logout_route(client, test_user):
    # Primeiro fazer login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Testar logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_add_task(client, test_user):
    # Primeiro fazer login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Adicionar tarefa
    response = client.post('/add_task', data={
        'title': 'Nova Tarefa',
        'description': 'Descricao da tarefa'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Nova Tarefa' in response.data

def test_admin_dashboard(client, test_user):
    # Primeiro fazer login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Tornar o usuário admin temporariamente
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        user.is_admin = True
        db.session.commit()
        
        # Garantir que o usuário está na sessão
        db.session.refresh(user)
    
    # Testar dashboard admin
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'Painel do Administrador' in response.data
