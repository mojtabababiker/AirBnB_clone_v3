#!/usr/bin/python3
"""
Route for status on object app_views
"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status:
    """
    return json status of object app_views
    """
    return jsonify({"status": "OK"})


@app.views.route('/stats')
def count():
    """
    retrieve number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
