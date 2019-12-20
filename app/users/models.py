from flask import current_app as app
from app import db, login
from app.status.models import Status
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

import jwt


# Create the table to track status subscriptions
subscribers = db.Table('subscribers',
                       db.Column('subscriber_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('subscribed_id', db.Integer,
                                 db.ForeignKey('trails.id'))
                       )

# Create the table to track reported statuses
reporters = db.Table('reporters',
                     db.Column('reporter_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('reported_id', db.Integer,
                               db.ForeignKey('status.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(200))
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    statuses = db.relationship('Status', backref='author', lazy='dynamic')

    subscribed = db.relationship(
        'Trails', secondary=subscribers,
        backref=db.backref('subscribers', lazy='dynamic'), lazy='dynamic')

    reported = db.relationship(
        'Status', secondary=reporters,
        backref=db.backref('reporter', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<user { self.username }>'

    def is_active(self):
        return User.query.filter_by(id=self.id).first().active

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def subscribe(self, trails):
        if not self.is_subscribed(trails):
            self.subscribed.append(trails)
            db.session.commit()

    def unsubscribe(self, trails):
        if self.is_subscribed(trails):
            self.subscribed.remove(trails)
            db.session.commit()

    def is_subscribed(self, trails):
        return self.subscribed.filter(subscribers.c.subscribed_id == trails.id).count() > 0

    def followed_statuses(self):
        return Status.query.join(subscribers,
                                 (subscribers.c.subscribed_id == Status.trail_system)).filter(
            subscribers.c.subscriber_id == self.id).order_by(Status.timestamp.desc())

    def report(self, status):
        if not self.has_reported(status):
            self.reported.append(status)
            db.session.commit()

    def has_reported(self, status):
        return self.reported.filter(reporters.c.reported_id == status.id).count() > 0

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
