import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    from src.app_factory import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_ui_admin(client):
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_home_ui_dataset_management(client):
    response = client.get('/dataset_management')
    assert response.status_code == 200
    assert b'Dataset Management' in response.data or b'dataset' in response.data.lower()

def test_history_borrow_history(client):
    response = client.get('/history')
    assert response.status_code == 200
    assert b'History' in response.data or b'history' in response.data.lower()

def test_demand_forecast_placeholder(client):
    # Demand Forecast button links to '#', so no route to test
    pass

def test_fine_calculation_placeholder(client):
    # Fine Calculation button links to '#', so no route to test
    pass

def test_manage_users_placeholder(client):
    # Manage Users button links to '#', so no route to test
    pass
