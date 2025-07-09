import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app

import pytest
from src.models import User
from src.app_factory import db, create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # Create admin user
        admin_user = User(username='admin', password='password', fullname='Admin User', email='admin@example.com')
        db.session.add(admin_user)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_admin_login_success(client):
    response = client.post('/admin/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome, Admin!' in response.data
    with client.session_transaction() as sess:
        assert sess['role'] == 'admin'
        assert 'user_id' in sess

def test_admin_login_failure(client):
    response = client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data

def test_admin_logout(client):
    # First login
    client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
    # Then logout
    response = client.get('/admin/logout', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess

def test_admin_dashboard_access_without_login(client):
    response = client.get('/admin', follow_redirects=True)
    # Since authentication is disabled for admin page, it should render admin page
    assert response.status_code == 200
    assert b'Welcome, Admin!' in response.data
