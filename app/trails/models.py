from app import db
from app.mixins import PaginatedAPIMixin


class Trails(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64))
    province = db.Column(db.String(2))
    trailforks = db.Column(
        db.String(128), default='https://www.trailforks.com')
    approved = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    statuses = db.relationship('Status', backref='trails', lazy='dynamic')

    def __repr__(self):
        return f'<Trail system { self.name }>'

    def activate(self):
        if not self.active:
            self.active = True
            db.session.commit()

    def deactivate(self):
        if self.active:
            self.active = False
            db.session.commit()

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'province': self.province,
            'approved:': self.approved,
            'trailforks': self.trailforks,
            'subscriber_count': self.subscribers.count(),
            'status_updates': self.statuses.count(),
            '_links': {
                'self': 'complete later',
                'status_updates': 'complete later',
                'subscribers': 'complete later'
            }
        }
        return data

    def from_dict(self, data, new_trails=False):
        for field in ['name', 'city', 'province', 'trailforks']:
            if field in data:
                setattr(self, field, data[field])
