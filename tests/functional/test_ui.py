import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_theme_toggle(driver):
    """Teste do toggle de tema claro/escuro"""
    driver.get('http://localhost:8080')
    
    # Encontrar o botão de tema
    theme_toggle = driver.find_element(By.CLASS_NAME, 'theme-toggle')
    
    # Verificar tema inicial
    body = driver.find_element(By.TAG_NAME, 'body')
    initial_theme = body.get_attribute('data-theme')
    
    # Clicar no botão
    theme_toggle.click()
    
    # Verificar se o tema mudou
    new_theme = body.get_attribute('data-theme')
    assert initial_theme != new_theme

def test_task_creation_ui(driver):
    """Teste da criação de tarefa pela UI"""
    driver.get('http://localhost:8080')
    
    # Login
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    username_input.send_keys('admin')
    password_input.send_keys('admin')
    submit_button.click()
    
    # Adicionar tarefa
    title_input = driver.find_element(By.NAME, 'title')
    description_input = driver.find_element(By.NAME, 'description')
    add_button = driver.find_element(By.CSS_SELECTOR, '.btn-primary')
    
    title_input.send_keys('UI Test Task')
    description_input.send_keys('Testing through Selenium')
    add_button.click()
    
    # Verificar se a tarefa aparece na lista
    task = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'UI Test Task')]"))
    )
    assert task is not None

def test_admin_dashboard_access(driver):
    """Teste de acesso ao painel do administrador"""
    driver.get('http://localhost:8080')
    
    # Login como admin
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    username_input.send_keys('admin')
    password_input.send_keys('admin')
    submit_button.click()
    
    # Verificar elementos do painel admin
    admin_elements = driver.find_elements(By.CLASS_NAME, 'admin-only')
    assert len(admin_elements) > 0
    
    # Verificar estatísticas
    stats = driver.find_elements(By.CLASS_NAME, 'stat-card')
    assert len(stats) > 0
