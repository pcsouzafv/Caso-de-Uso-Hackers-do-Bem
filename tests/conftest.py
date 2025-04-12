import pytest
import os
import sys
import tempfile
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Adicionar o diretório pai ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importando a instância singleton do SQLAlchemy
from db import db

# Importar do gerenciador centralizado de modelos
from models_manager import MainUser, MainTask, MainSystemLog, setup_test_db, cleanup_test_db

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def test_app():
    """Fixture que configura o app de teste"""
    try:
        # Tenta importar da versão principal (porta 8080)
        from app import create_app
        app = create_app('testing')
    except (ImportError, TypeError):
        try:
            # Se falhar, tenta importar da versão task_manager (porta 5000)
            from task_manager import create_app
            app = create_app(test_config={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        except ImportError:
            pytest.fail("Não foi possível importar create_app de nenhum módulo.")
    
    # Criar banco de dados temporário
    with app.app_context():
        # Configurar o banco de dados usando as funções do gerenciador centralizado
        setup_test_db()
        
        yield app
        
        # Limpar o banco de dados após os testes
        cleanup_test_db()

@pytest.fixture(scope="function")
def client(test_app):
    """Fixture que retorna um cliente de teste para a aplicação Flask"""
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def test_user(test_app):
    """Fixture que cria um usuário de teste"""
    with test_app.app_context():
        # Verificar se o usuário já existe e removê-lo
        existing_user = MainUser.query.filter_by(username="testuser").first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            
        # Criar um novo usuário
        user = MainUser(username="testuser", email="testuser@example.com")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        
        # Importante: obter uma versão atualizada do objeto após commit para evitar DetachedInstanceError
        user_refreshed = MainUser.query.get(user.id)
        
        yield user_refreshed
        
        # Limpar após o teste
        db.session.delete(user_refreshed)
        db.session.commit()

@pytest.fixture(scope="function")
def test_task(test_app, test_user):
    """Fixture que cria uma tarefa de teste"""
    with test_app.app_context():
        task = MainTask(title="Test Task", description="Test description", user_id=test_user.id)
        db.session.add(task)
        db.session.commit()
        
        # Importante: obter uma versão atualizada do objeto após commit para evitar DetachedInstanceError
        task_refreshed = MainTask.query.get(task.id)
        
        yield task_refreshed
        
        # Limpar após o teste
        db.session.delete(task_refreshed)
        db.session.commit()

@pytest.fixture(scope="function")
def test_system_log(test_app, test_user):
    """Fixture que cria um log de sistema de teste"""
    with test_app.app_context():
        log = MainSystemLog(action="Test action", details="Test details", user_id=test_user.id)
        db.session.add(log)
        db.session.commit()
        
        # Importante: obter uma versão atualizada do objeto após commit para evitar DetachedInstanceError
        log_refreshed = MainSystemLog.query.get(log.id)
        
        yield log_refreshed
        
        # Limpar após o teste
        db.session.delete(log_refreshed)
        db.session.commit()

@pytest.fixture(scope="function")
def live_server(test_app):
    """Fixture que inicia o servidor Flask em modo de teste"""
    port = 5000
    server = threading.Thread(
        target=test_app.run,
        kwargs={
            'port': port,
            'use_reloader': False
        }
    )
    server.daemon = True
    server.start()
    yield f'http://localhost:{port}'
    server.join()

@pytest.fixture(scope="function")
def selenium_driver():
    """Configuração do Selenium WebDriver com diretório temporário único"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    except (webdriver.WebDriverException, ImportError, OSError) as e:
        logger.error("Erro ao inicializar o Selenium: %s", e)
        pytest.skip("Selenium não está disponível neste ambiente")
