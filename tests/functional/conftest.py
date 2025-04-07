import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def browser():
    """Fixture que configura o navegador para testes funcionais"""
    try:
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(service=service, options=options)
        browser.set_window_size(1920, 1080)
        yield browser
    finally:
        browser.quit()

@pytest.fixture(scope="module")
def live_server():
    """Fixture que inicia o servidor de desenvolvimento"""
    from app import app
    app.config['TESTING'] = True
    app.config['LIVE_SERVER_PORT'] = 0  # Usar uma porta aleatória
    server = app.test_client()
    ctx = app.app_context()
    ctx.push()
    app.test_client()
    yield server
    ctx.pop()
