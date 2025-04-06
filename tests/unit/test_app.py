# -*- coding: utf-8 -*-
import pytest
from app import app, db
from app.models import User, Task
from tests.conftest import client, test_app, test_user

@pytest.mark.unit
def test_home_page(client):
    """Test home page"""
    response = client.get('/')
    assert response.status_code == 302

    # Test login redirect
    assert b'Redirecting...' in response.data

@pytest.mark.unit
def test_login(client, test_user):
    # Test login with correct credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tasks' in response.data

    # Test login with incorrect credentials
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

@pytest.mark.unit
def test_register(client):
    # Test registration with valid data
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'securepass',
        'confirm_password': 'securepass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tasks' in response.data

    # Test registration with non-matching passwords
    response = client.post('/register', data={
        'username': 'user2',
        'email': 'user2@example.com',
        'password': 'pass1',
        'confirm_password': 'pass2'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Passwords do not match' in response.data

@pytest.mark.unit
def test_add_task(client, test_user):
    # Log in
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    # Test adding task
    response = client.post('/add_task', data={
        'title': 'Test Task',
        'description': 'This is a test task'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data
