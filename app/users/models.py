from app import db, login
from app.status.models import Status
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Create the table to track status subscriptions
subscribers = db.Table('subscribers',
                       db.Column('subscriber_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('subscribed_id', db.Integer,
                                 db.ForeignKey('trails.id'))
                       )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    statuses = db.relationship('Status', backref='author', lazy='dynamic')

    subscribed = db.relationship(
        'Trails', secondary=subscribers,
        backref=db.backref('subscribed', lazy='dynamic'), lazy='dynamic')

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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
