from app import db


class Trails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64))
    province = db.Column(db.String(2))
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
