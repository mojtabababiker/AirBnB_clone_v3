#!/usr/bin/python3
"""
API app model, version 1
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_restful import Api, Resource
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_session(err=None):
    """Handle the request teardown, and call storage.close()
       in each one"""
    try:
        storage.close()
    except Exception:
        pass

@app.errorhandler(404)
def handle_404(err=None):
    """
    Handle the 404 error for the API
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default='5000'))
    app.run(host=host, port=port, threaded=True)
