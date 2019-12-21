from datetime import datetime
from app import db


class Status(db.Model):
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
