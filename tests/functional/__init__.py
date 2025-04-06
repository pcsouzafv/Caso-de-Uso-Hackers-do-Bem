"""Testes funcionais para a interface do usuário"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser():
    """Fixture que configura o navegador para testes funcionais"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def live_server():
    """Fixture que inicia o servidor de desenvolvimento"""
    from app import app
    with app.test_client() as client:
        yield client
