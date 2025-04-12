import pytest
import os
import sys

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar diretamente do models_manager em vez do app.py
from models_manager import (
    MainUser, MainTask, MainSystemLog, 
    setup_test_db, create_test_user,
    create_test_task, create_test_log, cleanup_test_db
)
from db import db

# Importar o app do app.py
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Extrair a aplicação do módulo importado
app = app_module.app

# Fixture que configura o banco de dados para os testes
@pytest.fixture(scope="module")
def setup_database():
    with app.app_context():
        # Usar as funções do models_manager
        setup_test_db()
        
        # Criar dados de teste
        user = create_test_user()
        create_test_task(user.id)
        create_test_log(user.id)
        
        yield
        
        # Limpar ao final
        cleanup_test_db()

@pytest.mark.unit
def test_user_creation(setup_database):
    """Test user creation"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'
        assert user.check_password('testpass')
        assert not user.check_password('wrongpass')
        assert user.is_admin is False

@pytest.mark.unit
def test_task_creation(setup_database):
    """Test task creation"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        task = MainTask.query.filter_by(user_id=user.id).first()
        assert task is not None
        assert task.title == 'Test Task'
        assert task.description == 'Test description'
        assert task.completed is False
        assert task.user_id == user.id
        assert task.created_at is not None

@pytest.mark.unit
def test_system_log_creation(setup_database):
    """Test system log creation"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        log = MainSystemLog.query.filter_by(user_id=user.id).first()
        assert log is not None
        assert log.action == 'Test action'
        assert log.details == 'Test details'
        assert log.user_id == user.id
        assert log.timestamp is not None

@pytest.mark.unit
def test_user_relationships(setup_database):
    """Test user relationships"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        assert len(user.tasks) > 0
        assert len(user.system_logs) > 0

@pytest.mark.unit
def test_task_relationships(setup_database):
    """Test task relationships"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        task = MainTask.query.filter_by(user_id=user.id).first()
        assert task.user == user

@pytest.mark.unit
def test_system_log_relationships(setup_database):
    """Test system log relationships"""
    with app.app_context():
        user = MainUser.query.filter_by(username="testuser").first()
        log = MainSystemLog.query.filter_by(user_id=user.id).first()
        assert log.user == user
