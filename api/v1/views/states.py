#!/usr/bin/python3
"""This is index views, route of blueprint"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify
@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """ Returns states """
    result = []
    data = storage.all(State)
    for obj in data.values():
        result.append((obj).to_dict())
    return jsonify(result)
