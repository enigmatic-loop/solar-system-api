from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    result = []

    all_planets = Planet.query.all()
    for planet in all_planets:
        # planet_dict = {
        #     "id": planet.id,
        #     "name": planet.name,
        #     "description": planet.description,
        #     "moon": planet.moon
        # }
        result.append(planet.to_dict())
    return jsonify(result), 200

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"planet {planet_id} invalid"}, 400))

    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        abort(make_response({"message": f"planet {planet_id} not found"}, 404))

    return chosen_planet


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return jsonify(planet.to_dict()), 200

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

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_one_planet(planet_id):
    update_planet = validate_planet(planet_id)

    request_body = request.get_json()

    try:
        update_planet.name = request_body["name"]
        update_planet.description = request_body["description"]
        update_planet.moon = request_body["moon"]
    except:
        return jsonify({"message": "Missing needed data"}), 400

    db.session.commit()

    return jsonify({"message": f"Successfully updated planet with id: {update_planet.id}"})

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    planet_to_delete = validate_planet(planet_id)

    request_body = request.get_json()

    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted planet with id: {planet_to_delete.id}"})