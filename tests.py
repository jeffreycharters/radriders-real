from datetime import datetime, timedelta
import unittest
from app import db, create_app
from app.users.models import User
from app.trails.models import Trails
from app.status.models import Status
from config import Config

import os

from coverage import coverage

cov = coverage(branch=True, omit=['flask/*', 'tests.py', 'venv/*'])
cov.start()


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


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

    def test_user(self):
        u1 = User(username='pete', email='pete@example.com')
        u2 = User(username='ruttiger', email='ruttiger@example.com')
        u3 = User(username='stampy', email='stampy@example.com')
        u4 = User(username='pipsqueak', email='pipsqueak@example.com')
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

    def test_password_hashing(self):
        u = User(username='shrednik')
        u.set_password('shreddies')
        self.assertFalse(u.check_password('catpee'))
        self.assertTrue(u.check_password('shreddies'))

    def test_subscribe(self):
        t1 = Trails(name='Trail System 1', city='City1',
                    province='ON', approved=True)
        t2 = Trails(name='Trail System 2', city='City2',
                    province='ON', approved=True)
        t3 = Trails(name='Trail System 3', city='City3',
                    province='BC', approved=True)
        t4 = Trails(name='Trail System 4', city='City4',
                    province='QC', approved=True)
        db.session.add_all([t1, t2, t3, t4])
        db.session.commit()

        print(User.query.all())
        u1, u2, u3, u4 = User.query.all()

        u1.subscribe(t1)
        u2.subscribe(t1)
        u2.subscribe(t2)
        u3.subscribe(t1)
        u3.subscribe(t2)
        u3.subscribe(t3)
        u4.subscribe(t4)
        db.session.commit()

        s1 = u1.subscribed.all()
        s2 = u2.subscribed.all()
        s3 = u3.subscribed.all()
        s4 = u4.subscribed.all()

        self.assertEqual(s1, [t1])
        self.assertEqual(s2, [t1, t2])
        self.assertEqual(s3, [t1, t2, t3])
        self.assertEqual(s4, [t4])


if __name__ == '__main__':
    try:
        unittest.main(verbosity=2)
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
