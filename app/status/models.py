from datetime import datetime
from app import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trail_system = db.Column(db.Integer, db.ForeignKey('trails.id'))

    def __repr__(self):
        return f'<Status {self.author, self.trails, self.body }>'
