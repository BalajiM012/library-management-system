import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import create_app, db
from src.models import BorrowRecord
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # Setup sample borrow record
        borrow = BorrowRecord(
            user_id=1,
            book_id=1,
            borrow_date=datetime.utcnow() - timedelta(days=10),
            due_date=datetime.utcnow() - timedelta(days=5),
            return_date=None,
            fine=0
        )
        db.session.add(borrow)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_borrow_records(client):
    response = client.get('/due_date_fine_tracking/api/borrow_records')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_return_book_and_fine(client):
    # Get borrow records to find borrow_id
    response = client.get('/due_date_fine_tracking/api/borrow_records')
    borrow_id = response.get_json()[0]['id']
    # Return book
    response = client.post(f'/due_date_fine_tracking/api/return_book/{borrow_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'fine' in data
    assert data['fine'] >= 0
