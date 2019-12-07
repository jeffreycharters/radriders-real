from app import db

class Trails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64))
    province = db.Column(db.String(64))
    statuses = db.relationship('Status', backref='trails', lazy='dynamic')
    
    def __repr__(self):
        return f'<Trail system { self.name }>'