import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    response = client.post('/user/login', json={'username': 'admin', 'password': 'password'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['username'] == 'admin'

def test_login_failure(client):
    response = client.post('/user/login', json={'username': 'admin', 'password': 'wrongpass'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
