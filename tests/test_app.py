import pytest
from app import app, db
from models import User, Task

@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def test_user(test_app):
    test_user = User(username='testuser', email='testuser@example.com', password_hash='testpass')
    test_user.set_password('testpass')
    with test_app.app_context():
        db.session.add(test_user)
        db.session.commit()
    return test_user

def test_home_page(client, test_user):
    # Primeiro, tenta acessar sem estar logado
    response = client.get('/')
    assert response.status_code == 302

    # Faz login com o usuário de teste
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Agora deve conseguir acessar a página inicial
    response = client.get('/')
    assert response.status_code == 200

def test_login(client, test_user):
    # Testa login com credenciais corretas
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Testa login com credenciais incorretas
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert response.status_code == 200
    assert b'<div class="alert alert-danger">Usu\xc3\xa1rio ou senha inv\xc3\xa1lidos</div>' in response.data
