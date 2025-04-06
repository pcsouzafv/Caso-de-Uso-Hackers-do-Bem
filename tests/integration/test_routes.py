import pytest
from app import app, db
from app.models import User, Task
from flask import url_for

@pytest.mark.integration
def test_login_route(client):
    """Test login route"""
    response = client.get(url_for('login'))
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_login_user(client, test_user):
    """Test user login"""
    response = client.post(url_for('login'), data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tasks' in response.data

@pytest.mark.integration
def test_logout_route(client, test_user):
    """Test user logout"""
    # First login
    client.post(url_for('login'), data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Now logout
    response = client.get(url_for('logout'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

@pytest.mark.integration
def test_add_task(client, test_user):
    """Test task addition"""
    # First login
    client.post(url_for('login'), data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Add task
    response = client.post(url_for('add_task'), data={
        'title': 'New Task',
        'description': 'Task description'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Task' in response.data

@pytest.mark.integration
def test_admin_dashboard(client, test_user):
    """Test admin dashboard"""
    # First login
    client.post(url_for('login'), data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    
    # Temporarily make user admin
    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        user.is_admin = True
        db.session.commit()
        
        # Ensure user is in session
        db.session.refresh(user)
    
    # Test admin dashboard
    response = client.get(url_for('admin'))
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
