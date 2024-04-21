#!/usr/bin/python3
"""Importing modules"""
import hashlib
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/users", strict_slashes=False, methods=["GET"])
def users(user_id=None):
    """list of all users objects or specific User """
    if user_id is None:
        result = []
        users = storage.all(User).values()
        for user in users:
            result.append(user.to_dict())
        return jsonify(result)
    else:
        user = storage.get(User, user_id)
        if user is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """ delete a User object that matches a <user_id>"""
    user = storage.get(User, user_id)
    if user is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def Create_user():
    """
    Create User
    """
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "email" not in json_data:
            return make_response("Missing email", 400)
        if "password" not in json_data:
            return make_response("Missing password", 400)
        instance = User(**json_data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """update user"""
    obj = storage.get(User, user_id)
    if obj is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response("Not a JSON", 400)
    obj.password = data.get("password", obj.password)
    obj.first_name = data.get("first_name", obj.first_name)
    obj.last_name = data.get("last_name", obj.last_name)
    obj.save()
    return jsonify(obj.to_dict()), 200
