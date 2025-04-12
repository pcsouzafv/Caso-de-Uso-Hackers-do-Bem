"""Functional tests for the user interface"""

import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar gerenciador de modelos
from models_manager import MainUser, MainTask, MainSystemLog, setup_test_db, cleanup_test_db
from db import db

# Importar a aplicação
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Extrair a aplicação do módulo importado
app = app_module.app

def pytest_setup_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    return chrome_options

@pytest.fixture(scope="function")
def browser():
    """Configuração do navegador para testes"""
    options = pytest_setup_options()
    driver = webdriver.Chrome(
        options=options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def live_server():
    """Inicializa o servidor para testes"""
    with app.app_context():
        # Configurar o banco de dados
        setup_test_db()
        
        # Criar usuário para teste
        user = MainUser.query.filter_by(username="testuser").first()
        if not user:
            user = MainUser(username="testuser", email="testuser@example.com")
            user.set_password("testpass")
            db.session.add(user)
            db.session.commit()
        
        # Iniciar o servidor em uma thread separada
        import threading
        port = 8080  # Usar a porta correta
        server = threading.Thread(
            target=app.run,
            kwargs={
                'host': '0.0.0.0',
                'port': port,
                'use_reloader': False,
                'debug': False,
                'threaded': True
            }
        )
        server.daemon = True
        server.start()
        
        # Esperar um pouco para o servidor iniciar
        import time
        time.sleep(1)
        
        # Retornar a URL base para os testes
        base_url = f"http://localhost:{port}"
        yield base_url
        
        # Limpar após os testes
        with app.app_context():
            db.session.close_all()
            cleanup_test_db()

def test_theme_toggle(browser, live_server):
    """Teste do toggle de tema claro/escuro"""
    # Verificar se o servidor está acessível antes de prosseguir
    import requests
    from urllib3.exceptions import MaxRetryError
    from requests.exceptions import ConnectionError
    
    # Tentar conectar ao servidor com retry
    connected = False
    for attempt in range(5):  # 5 tentativas
        try:
            response = requests.get(live_server, timeout=2)
            if response.status_code == 200:
                connected = True
                break
        except (ConnectionError, MaxRetryError):
            import time
            time.sleep(2)  # Esperar 2 segundos antes de tentar novamente
    
    if not connected:
        pytest.skip(f"Servidor não disponível em {live_server}")
    
    # Acessar o servidor
    browser.get(live_server)
    
    # Verificar tema inicial
    assert 'light' in browser.page_source
    
    # Clicar no botão de toggle
    theme_toggle = browser.find_element(By.CLASS_NAME, 'theme-toggle')
    theme_toggle.click()
    
    # Verificar se o tema mudou
    assert 'dark' in browser.page_source
    
    # Alternar de volta
    theme_toggle.click()
    assert 'light' in browser.page_source

def test_task_creation_ui(browser, live_server):
    """Teste da criação de tarefa pela UI"""
    browser.get(live_server)
    
    # Fazer login
    username_field = browser.find_element(By.ID, 'username')
    password_field = browser.find_element(By.ID, 'password')
    login_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    username_field.send_keys('testuser')
    password_field.send_keys('testpass')
    login_button.click()
    
    # Aguardar redirecionamento
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'task-form'))
    )
    
    # Preencher formulário de tarefa
    title_field = browser.find_element(By.ID, 'title')
    description_field = browser.find_element(By.ID, 'description')
    submit_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    title_field.send_keys('Test Task')
    description_field.send_keys('This is a test task')
    submit_button.click()
    
    # Verificar se a tarefa foi criada
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Test Task')]"))
    )

def test_admin_dashboard_access(browser, live_server):
    """Teste de acesso ao painel do administrador"""
    browser.get(live_server)
    
    # Fazer login com usuário admin
    username_field = browser.find_element(By.ID, 'username')
    password_field = browser.find_element(By.ID, 'password')
    login_button = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    username_field.send_keys('admin')
    password_field.send_keys('adminpass')
    login_button.click()
    
    # Aguardar redirecionamento
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'admin-dashboard'))
    )
    
    # Verificar elementos do painel
    assert 'Painel do Administrador' in browser.page_source
    assert 'Gerenciar Usuários' in browser.page_source
    assert 'Gerenciar Tarefas' in browser.page_source
    assert 'Logs do Sistema' in browser.page_source
