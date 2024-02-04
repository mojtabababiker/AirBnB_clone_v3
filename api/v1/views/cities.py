#!/usr/bin/python3
"""
API /cities route for version v1
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort


@app_views.get('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """
    API route to retirve all cities instance that belong to
    state with state_id
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []

    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)

@app_views.get('/cities/<city_id>', strict_slashes=False)
def cities_get_city(city_id):
    """
    API route to retrive city instance from the database
    with the id city_id
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())

@app_views.delete('/cities/<city_id>', strict_slashes=False)
def cities_delete_city(city_id):
    """
    API route to delete city instance from the database
    with the id city_id
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify(dict()), 200

@app_views.post('/states/<state_id>/cities', strict_slashes=False)
def cities_set_state_city(state_id):
    """
    API route to set a new city instance to the database under
    the state with the id state_id
    """
    from models.city import City

    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
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

@app_views.put('/cities/<city_id>', strict_slashes=False)
def cities_update_city(city_id):
    """
    API route to update a city instance from the database under
    the id city_id
    """
    if not request.json:
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
