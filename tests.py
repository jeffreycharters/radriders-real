from datetime import datetime, timedelta
import unittest
from app import db, create_app
from app.users.models import User
from app.trails.models import Trails
from app.status.models import Status
from config import Config

class TestConfig(Config):
    TESTING = TrueSQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
        def setUp(self):
            self.app = create_app(TestConfig)
            self.app_context = self.app.app_context()
            self.app_context.push()
            db.create_all()

        def tearDown(self):
            db.session.remove()
            db.drop_all()
            self.app_context.pop()

        def test_password_hashing(self):
            u = User(username='shrednik')
            u.set_password('shreddies')
            self.assertFalse(u.check_password('catpee'))
            self.assertTrue(u.check_password('shreddies'))

if __name__ == '__main__':
    unittest.main(verbosity=2)