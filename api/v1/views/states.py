#!/usr/bin/python3
"""
API /states route for version v1
"""
# from api.v1.views import app_views, storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False)
def states_get_all():
    """
    API route returns the all instances of states on
    The database
    """
    from api.v1.app import storage
    states_dict = storage.all("State")
    states = []

    for state in states_dict.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states', strict_slashes=False,
                 methods=["POST"])
def states_set_new():
    """
    API route set a new instance of states to
    The database
    """
    from api.v1.app import storage
    from models.state import State
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'name' not in request.json:
        abort(400, description="Missing name")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_get_state(state_id):
    """
    API route get an instance of states from
    The database according to its id
    """
    from api.v1.app import storage
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=["DELETE"])
def states_del_state(state_id):
    """
    API route get an instance of states from
    The database according to its id
    """
    from api.v1.app import storage
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify(dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=["PUT"])
def states_update_state(state_id):
    """
    API route set a new instance of states to
    The database
    """
    from api.v1.app import storage
    from models.state import State

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    for key, val in kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
