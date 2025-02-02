#!/usr/bin/python3
"""
API /amenities route for version v1
"""
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False)
def amenities_get_all():
    """
    API route to retrive all amenities instances from database
    """
    from api.v1.app import storage
    amenities = storage.all('Amenity')
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenities_get_amenity(amenity_id):
    """
    API route to rerive amenity instance from database with
    the id amenity_id
    """
    from api.v1.app import storage
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["DELETE"])
def amenities_del_amenity(amenity_id):
    """
    API route to delete amenity instance from database with
    the is amenity_id
    """
    from api.v1.app import storage
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    return jsonify(dict())


@app_views.route('/amenities', strict_slashes=False,
                 methods=["POST"])
def amenities_set_amenity():
    """
    API route to set a new instance of amenity
    """
    from api.v1.app import storage
    from models.amenity import Amenity

    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    if 'name' not in request.json:
        abort(400, description='Missing name')
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=["PUT"])
def amenities_update_amenity(amenity_id):
    """
    API route to update amenity instance on the database with
    id amenity_id
    """
    from api.v1.app import storage
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    for key, val in kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())
