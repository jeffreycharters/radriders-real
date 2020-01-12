from flask import url_for
from datetime import datetime
from app import db

from app.mixins import PaginatedAPIMixin


class Status(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trail_system = db.Column(
        db.Integer, db.ForeignKey('trails.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Status { self.author, self.trails, self.body }>'

    def activate(self):
        if not self.active:
            self.active = True
            db.session.commit()

    def deactivate(self):
        if self.active:
            self.active = False
            db.session.commit()

    def deactivate_if_necessary(self):
        report_count = self.reporter.count()
        if report_count > 4:
            self.deactivate()

    def to_dict(self):
        data = {
            'id': self.id,
            'author': self.user_id,
            'trail_system': self.trail_system,
            'body': self.body,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'active': self.active,
            'reported_count': self.reporter.count(),
            '_links': {
                'self': url_for('api.get_status', id=self.id),
                'author': url_for('api.get_user', id=self.author.id),
                'trails': url_for('api.get_trails', id=self.trails.id)

            }

        }
        return data

    def from_dict(self, data):
        for field in ['author', 'trail_system', 'body']:
            if field in data:
                setattr(self, field, data[field])
