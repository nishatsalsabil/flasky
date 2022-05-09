from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver = db.Column(db.String)
    team = db.Column(db.String)
    mass_kg = db.Column(db.Integer)