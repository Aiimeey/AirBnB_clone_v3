#!/usr/bin/python3
"""This is index views, route of blueprint"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """return a JSON: list of all State objects or one State,
    Or not found if id not exsit"""
    if state_id is None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)
    else:
        result = []
        key = f"State.{state_id}"
        states = storage.all(State)[key]
        return jsonify(states.to_dict())

