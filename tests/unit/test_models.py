import pytest
import os
import sys

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar diretamente do arquivo app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))))
from db import db

# Precisamos importar o app diretamente do arquivo root app.py, não do pacote app/
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Extrair os modelos e a aplicação do módulo importado
User = app_module.User
Task = app_module.Task
SystemLog = app_module.SystemLog
app = app_module.app

# Fixture que configura o banco de dados para os testes
@pytest.fixture(scope="module")
def setup_database():
    with app.app_context():
        # Criar tabelas no banco de dados
        db.create_all()
        
        # Verificar se o banco de dados já tem dados
        existing_admin = User.query.filter_by(username='admin').first()
        existing_testuser = User.query.filter_by(username='testuser').first()
        
        # Obter ou criar usuário de teste
        if existing_testuser:
            user = existing_testuser
        else:
            user = User(username="testuser", email="testuser@example.com", is_admin=False)
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()
        
        # Criar tarefa de teste
        task = Task(
            title="Test Task",
            description="Test description",
            completed=False,
            user_id=user.id
        )
        db.session.add(task)
        
        # Criar log de sistema de teste
        log = SystemLog(
            action="Test action",
            details="Test details",
            user_id=user.id
        )
        db.session.add(log)
        
        # Commit das alterações
        db.session.commit()
        
        yield
        
        # Limpeza após os testes (não removemos o admin padrão)
        tasks_to_remove = Task.query.filter_by(title="Test Task").all()
        logs_to_remove = SystemLog.query.filter_by(action="Test action").all()
        
        for task in tasks_to_remove:
            db.session.delete(task)
        
        for log in logs_to_remove:
            db.session.delete(log)
            
        db.session.commit()

@pytest.mark.unit
def test_user_creation(setup_database):
    """Test user creation"""
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
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
        user = User.query.filter_by(username="testuser").first()
        task = Task.query.filter_by(user_id=user.id).first()
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
        user = User.query.filter_by(username="testuser").first()
        log = SystemLog.query.filter_by(user_id=user.id).first()
        assert log is not None
        assert log.action == 'Test action'
        assert log.details == 'Test details'
        assert log.user_id == user.id
        assert log.timestamp is not None

@pytest.mark.unit
def test_user_relationships(setup_database):
    """Test user relationships with tasks and logs"""
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        
        # Verifica se há pelo menos uma tarefa e logs associados ao usuário
        assert len(user.tasks) > 0
        assert len(user.system_logs) > 0
        
        # Verifica se pelo menos uma tarefa tem o título esperado
        task_found = False
        for task in user.tasks:
            if task.title == 'Test Task':
                task_found = True
                break
        assert task_found, "Nenhuma tarefa com o título 'Test Task' encontrada para o usuário"
        
        # Verifica se pelo menos um log tem a ação esperada
        log_found = False
        for log in user.system_logs:
            if log.action == 'Test action':
                log_found = True
                break
        assert log_found, "Nenhum log com a ação 'Test action' encontrado para o usuário"

@pytest.mark.unit
def test_task_relationships(setup_database):
    """Test task relationships with user"""
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        task = Task.query.filter_by(user_id=user.id, title="Test Task").first()
        assert task.user.username == 'testuser'

@pytest.mark.unit
def test_system_log_relationships(setup_database):
    """Test system log relationships with user"""
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        log = SystemLog.query.filter_by(user_id=user.id, action="Test action").first()
        assert log.user.username == 'testuser'
