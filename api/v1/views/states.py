#!/usr/bin/python3
"""This is index views, route of blueprint"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, make_response, request


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """return list of all State objects or one State """
    if state_id is None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)
    else:
        key = f"State.{state_id}"
        try:
            state = storage.all(State)[key]
            return jsonify(state.to_dict())
        except KeyError:
            return jsonify({"error": "Not found"}), 404


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_states(state_id):
    """return a JSON: delete a state object that match State_id
    """
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def Create_state():
    """Creates a new State."""
    json_data = request.get_json(force=True, silent=True)
    if json_data:
        if "name" in json_data:
            instance = State(**json_data)
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
        else:
            return make_response("Missing name", 400)
    else:
        return make_response("Not a JSON", 400)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def Update_state(state_id):
    """ update state"""
    data = request.get_json()
    if data:
        obj = storage.get(State, state_id)
        if obj:
            obj.name = data.get("name", obj.name)
            obj.save()
            return jsonify(obj.to_dict()), 200
        else:
            return make_response(jsonify({"error": "Not found"}), 404)
    else:
        return make_response("Not a JSON", 400)
