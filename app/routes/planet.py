from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet

# class Planet:
#     def __init__(self, id, name, description, size):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.moon = moon

# planets = [
#     Planet(1, "Saturn", "has icy rings", 36184),
#     Planet(2, "Jupiter", "massive and has red spot", 43441),
#     Planet(3, "Uranus", "spins on side", 15759)
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    result = []

    all_planets = Planet.query.all()
    for planet in all_planets:
        planet_dict = {
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moon": planet.moon
        }
        result.append(planet_dict)
    return jsonify(result), 200

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message": f"planet {planet_id} invalid"}, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet

#     abort(make_response({"message": f"planet {planet_id} not found"}, 404))


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "moon": planet.moon
    }

@planets_bp.route("", methods=["POST"])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name = request_body['name'],
        description = request_body['description'],
        moon = request_body['moon']
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": f"Succesfully created Planet with id = {new_planet.id}"}), 201