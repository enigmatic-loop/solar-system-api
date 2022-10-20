from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, size):
        self.id = id
        self.name = name
        self.description = description
        self.size = size

planets = [
    Planet(1, "Saturn", "has icy rings", 36184),
    Planet(2, "Jupiter", "massive and has red spot", 43441),
    Planet(3, "Uranus", "spins on side", 15759)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    result = []
    for planet in planets:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "size": planet.size
        }
        result.append(planet_dict)
    return jsonify(result), 200
