from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    mass_kg = db.Column(db.Integer)
    #driver = db.relationship("Driver", backref="cars")


    def to_dict(self):
        return {
            "id": self.id,
            "driver": self.driver.name,
            "team": self.driver.team,
            "mass_kg": self.mass_kg
        }

    def to_dict_basic(self):
        return {
            "id": self.id,
            "mass_kg": self.mass_kg
        }
