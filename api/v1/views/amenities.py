#!/usr/bin/python3
"""Amenity module"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, make_response, request


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id=None):
    """ get amenity method """
    amenities = storage.all(Amenity)
    if amenities:
        if amenity_id is None:
            result = []
            for obj in amenities.values():
                result.append(obj.to_dict())
            return jsonify(result), 200
        else:
            key = f"Amenity.{amenity_id}"
            try:
                amenities = storage.all(Amenity)[key]
                if amenities.id == amenity_id:
                    return jsonify(amenities.to_dict()), 200
            except KeyError:
                return make_response(jsonify({"error": "Not found"}), 404)
    else:
        return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenities(amenity_id=None):
    """ delete amenity module """
    data = storage.get(Amenity, amenity_id)
    if data is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(data)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def Create_Amenity():
    """Creates a new Amenity """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "name" in json_data:
            instance = Amenity(**json_data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        else:
            return make_response("Missing name", 400)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """update amenity"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
