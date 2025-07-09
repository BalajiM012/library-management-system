import unittest
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app_factory import create_app, db
from src.models import User

class ManageUsersAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a test user with fullname to satisfy NOT NULL constraint
            user = User(fullname='Test User', username='testuser', email='test@example.com', password='testpass')
            db.session.add(user)
            db.session.commit()
            self.test_user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users(self):
        response = self.client.get('/manage_users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_user(self):
        response = self.client.get(f'/manage_users/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')

    def test_create_user(self):
        new_user = {
            'fullname': 'New User',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass'
        }
        response = self.client.post('/manage_users/', data=json.dumps(new_user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('user_id', data)

    def test_update_user(self):
        update_data = {
            'email': 'updated@example.com'
        }
        response = self.client.put(f'/manage_users/{self.test_user_id}', data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User updated')

    def test_delete_user(self):
        response = self.client.delete(f'/manage_users/{self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User deleted')

if __name__ == '__main__':
    unittest.main()
