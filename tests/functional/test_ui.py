"""Functional tests for the user interface"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from geckodriver_autoinstaller import install as gecko_install

def pytest_setup_options():
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    return firefox_options

@pytest.fixture(scope="function")
def browser():
    """Fixture que configura o navegador para os testes funcionais"""
    options = pytest_setup_options()
    service = Service(gecko_install())
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()

@pytest.mark.functional
def test_user_login(browser, live_server, test_user):
    """Test user login through the interface"""
    browser.get(f"{live_server}/login")
    
    # Fill in the login form
    username = browser.find_element(By.NAME, "username")
    password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
    username.send_keys("testuser")
    password.send_keys("testpass")
    submit.click()
    
    # Check if the user was redirected to the home page
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "task-list"))
    )
    
    assert browser.current_url == f"{live_server}/"
    assert "Tasks" in browser.page_source

@pytest.mark.functional
def test_create_task(browser, live_server, test_user):
    """Test task creation through the interface"""
    browser.get(f"{live_server}/login")
    
    # Login first
    username = browser.find_element(By.NAME, "username")
    password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
    username.send_keys("testuser")
    password.send_keys("testpass")
    submit.click()
    
    # Wait for login to complete
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "task-list"))
    )
    
    # Click the button to create a new task
    new_task_btn = browser.find_element(By.ID, "new-task-btn")
    new_task_btn.click()
    
    # Fill in the new task form
    title = browser.find_element(By.NAME, "title")
    description = browser.find_element(By.NAME, "description")
    submit = browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
    
    title.send_keys("Test Task")
    description.send_keys("This is a test task")
    submit.click()
    
    # Check if the task was created successfully
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "task-item"))
    )
    
    assert "Test Task" in browser.page_source
    assert "This is a test task" in browser.page_source
