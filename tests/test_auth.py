"""Test authentication routes."""
import pytest
from app.models import User


def test_register_user(client):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'full_name': 'Test User',
        'bio': 'Test bio'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify user was created
    with client.application.app_context():
        user = User.find_by_email('test@example.com')
        assert user is not None
        assert user['full_name'] == 'Test User'
        assert user['role'] == 'user'


def test_register_admin_user(client):
    """Test admin user registration."""
    response = client.post('/auth/register', data={
        'email': 'ashchugh@gmail.com',
        'password': 'Admin123!@#',
        'full_name': 'Admin User',
        'bio': 'Admin bio'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify admin role
    with client.application.app_context():
        user = User.find_by_email('ashchugh@gmail.com')
        assert user is not None
        assert user['role'] == 'admin'


def test_register_duplicate_email(client):
    """Test registration with duplicate email."""
    # Register first user
    client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'full_name': 'Test User'
    })
    
    # Try to register again
    response = client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test456!@#',
        'full_name': 'Another User'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'already registered' in response.data


def test_register_weak_password(client):
    """Test registration with weak password."""
    response = client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'weak',
        'full_name': 'Test User'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Password' in response.data


def test_login_success(client):
    """Test successful login."""
    # Register user first
    client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'full_name': 'Test User'
    })
    
    # Login
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test123!@#'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # Register user first
    client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'full_name': 'Test User'
    })
    
    # Login with wrong password
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid' in response.data


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'Test123!@#'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid' in response.data


def test_logout(client):
    """Test logout."""
    # Register and login
    client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'full_name': 'Test User'
    })
    
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test123!@#'
    })
    
    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
