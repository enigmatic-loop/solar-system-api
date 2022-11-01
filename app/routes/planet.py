from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    moon_query_value = request.args.get("moon")

    if moon_query_value is not None:
        planets = Planet.query.filter_by(moon=moon_query_value)
    else:
        planets = Planet.query.all()

    result_planet = [planet.to_dict() for planet in planets]

    return jsonify(result_planet), 200


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
        for key, value in request_body.items():
            if value not in request_body:
                return jsonify({"message": f"{key} is missing"}), 400


        # if "name" not in request_body:
        #     return jsonify({"message": f"Planet name is missing"}), 400
        # elif "description" not in request_body:
        #     return jsonify({"message": f"Description is missing"}), 400
        # else:
        #     return jsonify({"message": f"Planet moon is missing"}), 400

    db.session.commit()

    return jsonify({"message": f"Successfully updated planet with id: {update_planet.id}"})

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    planet_to_delete = validate_planet(planet_id)

    request_body = request.get_json()

    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted planet with id: {planet_to_delete.id}"})