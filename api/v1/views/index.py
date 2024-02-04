#!/usr/bin/python3
"""
API /status route for version v1
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def api_status():
    """
    API route returns the status of the API itself
    """
    return jsonify({"status": "OK"})


@app_views.route('/state', strict_slashes=False)
def api_statistics():
    """
    API route returns the count of all instances on
    The database
    """
    stats = {"amenities": "Amenity", "cities": "City", "places": "Place",
             "reviews": "Review", "states": "State", "users": "User"}

    for key, val in stats.items():
        stats[key] = storage.count(val)

    return jsonify(stats)
