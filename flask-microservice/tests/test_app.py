import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login(self):
        response = self.app.post('/login', data=dict(username='testuser', password='testpass'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'JWT Token', response.data)

    def test_register(self):
        response = self.app.post('/register', data=dict(username='newuser', password='newpass'))
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Registration successful', response.data)

    def test_fetch_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book List', response.data)

if __name__ == '__main__':
    unittest.main()