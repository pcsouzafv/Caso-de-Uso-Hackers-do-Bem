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
    """Cria um usuário de teste na sessão do banco de dados.
    Importante: este fixture deve ser usado APENAS dentro de um contexto app.app_context().
    """
    # Criar o usuário - importante que isso seja feito FORA de app_context
    # para garantir que o usuário seja criado, mas não vincule a sessão atual
    user = MainUser(username="testuser", email="testuser@example.com")
    user.set_password("testpass")
    
    # Dentro de app_context, salvamos o usuário e o recuperamos para garantir
    # que ele seja persistido na sessão atual
    with app.app_context():
        # Limpar qualquer usuário existente com o mesmo nome
        existing = MainUser.query.filter_by(username="testuser").first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
        
        # Adicionar e persistir o novo usuário
        db.session.add(user)
        db.session.commit()
        
        # Importante: recuperar o usuário do banco para garantir que ele esteja
        # vinculado à sessão atual
        fresh_user = MainUser.query.filter_by(username="testuser").first()
        
        yield fresh_user  # Retorna o usuário recuperado da sessão atual
        
        # Limpar após o teste
        user_to_delete = MainUser.query.filter_by(username="testuser").first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()

@pytest.mark.integration
def test_login_route(client):
    """Test login route"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_login_user(client, test_user):
    """Test user login"""
    # Não é necessário usar o app_context aqui, pois o fixture test_user já garante
    # que o usuário está corretamente persistido
    response = client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Tarefas' in response.data or b'Task' in response.data

@pytest.mark.integration
def test_logout_route(client, test_user):
    """Test user logout"""
    # Fazer login primeiro
    client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Agora fazer logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_add_task(client, test_user):
    """Test task addition"""
    # Primeiro fazer login
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
    # Definir o usuário como admin no contexto apropriado
    with app.app_context():
        # Recuperar o usuário para garantir que esteja na sessão atual
        user = MainUser.query.filter_by(username="testuser").first()
        user.is_admin = True
        db.session.commit()
    
    # Fazer login
    client.post('/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Testar o dashboard admin
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
