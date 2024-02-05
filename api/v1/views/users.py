#!/usr/bin/python3
"""
API /users route for version v1
"""
# from api.v1.views import app_views, storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.get('/users', strict_slashes=False)
def users_get_all():
    """
    API route to retrive all users instances from database
    """
    from api.v1.app import storage
    users = storage.all('User')
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.get('/users/<user_id>', strict_slashes=False)
def users_get_user(user_id):
    """
    API route to rerive user instance from database with
    the id user_id
    """
    from api.v1.app import storage
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.delete('/users/<user_id>', strict_slashes=False)
def users_del_user(user_id):
    """
    API route to delete user instance from database with
    the is user_id
    """
    from api.v1.app import storage
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    storage.delete(user)
    return jsonify(dict())


@app_views.post('/users', strict_slashes=False)
def users_set_user():
    """
    API route to set a new instance of user
    """
    from api.v1.app import storage
    from models.user import User

    if not request.json:
        abort(400, description='Not a JSON')
    if 'email' not in request.json:
        abort(400, description='Missing email')
    if 'password' not in request.json:
        abort(400, description='Missing password')
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.put('/users/<user_id>', strict_slashes=False)
def users_update_user(user_id):
    """
    API route to update user instance on the database with
    id user_id
    """
    from api.v1.app import storage
    if not request.json:
        abort(400, description="Not a JSON")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    for key, val in kwargs.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict())
