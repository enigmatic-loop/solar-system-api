from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    moon = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "moon": self.moon
        }

    @classmethod
    def from_dict(cls, planet_dict):
        return cls(
            name=planet_dict["name"],
            description=planet_dict["description"],
            moon=planet_dict["moon"]
        )