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
        db.create_all()

        # Criar usuário para teste
        test_user = MainUser.query.filter_by(username="testuser").first()
        if not test_user:
            test_user = MainUser(username="testuser", email="testuser@example.com")
            test_user.set_password("testpass")
            db.session.add(test_user)
            
        # Criar usuário admin
        admin_user = MainUser.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = MainUser(username="admin", email="admin@example.com", is_admin=True)
            admin_user.set_password("adminpass")
            db.session.add(admin_user)
            
        db.session.commit()
        
    # Iniciar servidor
    port = 8080
    thread = app.app_context()
    thread.__enter__()
    
    yield f"http://localhost:{port}"
    
    # Limpar
    thread.__exit__(None, None, None)
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_theme_toggle(browser, live_server):
    """Teste do toggle de tema claro/escuro"""
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
