from app import db

class Trails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64))
    
    def __repr__(self):
        return f'<Trail system { self.body }>'