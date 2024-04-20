#!/usr/bin/python3
"""City module"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, make_response, request


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_state_cities(state_id=None):
    """ get state cities method """
    cities = storage.all(City)
    if cities:
        result = []
        for value in cities.values():
            if value.state_id == state_id:
                result.append(value.to_dict())
        return jsonify(value.to_dict()), 200
    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id=None):
    """ get city method"""
    key = f"City.{city_id}"
    try:
        city = storage.all(City)[key]
        return jsonify(city.to_dict())
    except KeyError:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id=None):
    """ delete city """
    key = f"City.{city_id}"
    try:
        city = storage.all(City)[key]
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except KeyError:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_city(state_id=None):
    """ post city method """
    data = request.get_json(force=True, silent=True)
    if data:
        key = f"State.{state_id}"
        try:
            state = storage.all(State)[key]
            if "name" in data:
                data['state_id'] = state_id
                instance = City(**data)
                instance.save()
                return make_response(jsonify(instance.to_dict()), 201)
            else:
                return make_response("Missing name", 400)
        except KeyError:
            return make_response(jsonify({"error": "Not found"}), 404)
    else:
        return make_response("Not a JSON", 400)


@app_views.route('/cities/<city_id>', strict_slashes=True, methods=['PUT'])
def put_city(city_id=None):
    """ put city method """
    data = request.get_json(force=True, silent=True)
    if data:
        key = f"City.{city_id}"
        try:
            city = storage.all(City)[key]
            city.name = data.get("name", city.name)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)
        except KeyError:
            return make_response(jsonify({"error": "Not found"}), 404)
    else:
        return make_response("Not a JSON", 400)
