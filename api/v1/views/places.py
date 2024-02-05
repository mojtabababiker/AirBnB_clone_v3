#!/usr/bin/python3
"""
API /places route for version v1
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort


@app_views.get('/cities/<city_id>/places', strict_slashes=False)
def places_get_city_places(city_id):
    """
    API route to retrive all places instance on the city with
    id city_id form database
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = []

    for place in places.values():
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.get('/places/<place_id>',  strict_slashes=False)
def places_get_place(place_id):
    """
    API to retirve a place instance from the database with
    the id place_id
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.delete('/places/<place_id>', strict_slashes=False)
def places_del_place(place_id):
    """
    API to delete a place instance from the database with
    the id place_id
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    storage.delete(place)
    return jsonify(dict())


@app_views.post('/cities/<city_id>/places', strict_slashes=False)
def places_set_city_places(city_id):
    """
    API route to add a new place instance on the city with
    id city_id to database
    """
    from models.place import Place
    if not request.json:
        abort(400, description="Not a JSON")
    if "user_id" not in request.json:
        abort(400, description="Missing user_id")
    if "name" not in request.json:
        abort(400, description="Missing name")

    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    kwargs["city_id"] = city_id

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    place = Place(**kwargs)
    return jsonify(place.to_dict()), 201


@app_views.put('/places/<place_id>', strict_slashes=False)
def places_update_place(place_id):
    """
    API route to update place instance with
    id place_id on database
    """
    from models.place import Place
    if not request.json:
        abort(400, description="Not a JSON")

    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    for key, val in kwargs.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict())