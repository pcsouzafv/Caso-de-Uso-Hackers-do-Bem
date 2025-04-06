# tests/conftest.py
import pytest
import os
import sys
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from task_manager import create_app, db
from task_manager.models import User, Task

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='function')
def selenium_driver():
    """Configuração do Selenium WebDriver com diretório temporário único"""
    options = Options()
    # Cria um diretório temporário único
    user_data_dir = tempfile.mkdtemp(prefix='selenium_')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--headless=new')  # Chrome 111+ usa 'new'
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # Configura o driver usando webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    # Limpa o driver e o diretório temporário
    driver.quit()
    import shutil
    shutil.rmtree(user_data_dir)

@pytest.fixture
def app():
    """Cria uma instância do app para testes"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Usuário de teste"""
    with app.app_context():
        user = User(username='test_user')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()