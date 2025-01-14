#!/usr/bin/python3
"""
API /cities route for version v1
"""
# from api.v1.views import app_views, storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["GET"])
def cities_by_state(state_id):
    """
    API route to retirve all cities instance that belong to
    state with state_id
    """
    from api.v1.app import storage
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []

    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["GET"])
def cities_get_city(city_id):
    """
    API route to retrive city instance from the database
    with the id city_id
    """
    from api.v1.app import storage
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["DELETE"])
def cities_delete_city(city_id):
    """
    API route to delete city instance from the database
    with the id city_id
    """
    from api.v1.app import storage
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify(dict()), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=["POST"])
def cities_set_state_city(state_id):
    """
    API route to set a new city instance to the database under
    the state with the id state_id
    """
    from api.v1.app import storage
    from models.city import City

    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=["PUT"])
def cities_update_city(city_id):
    """
    API route to update a city instance from the database under
    the id city_id
    """
    from api.v1.app import storage
    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    for key, val in kwargs.items():
        if key not in ["id", "state_id", "created_at",
                       "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
