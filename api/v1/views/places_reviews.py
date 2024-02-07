#!/usr/bin/python3
"""
API /reviews route for version v1
"""
# from api.v1.views import app_views, storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_by_place(place_id):
    """
    API route to retirve all reviews instance that belong to
    place with place_id
    """
    from api.v1.app import storage
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []

    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def reviews_get_review(review_id):
    """
    API route to retrive review instance from the database
    with the id review_id
    """
    from api.v1.app import storage
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=["DELETE"])
def reviews_delete_review(review_id):
    """
    API route to delete review instance from the database
    with the id review_id
    """
    from api.v1.app import storage
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return jsonify(dict()), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=["POST"])
def reviews_set_place_review(place_id):
    """
    API route to set a new review instance to the database under
    the place with the id place_id
    """
    from api.v1.app import storage
    from models.review import Review

    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    if 'text' not in request.json:
        abort(400, description="Missing text")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    user = storage.get("User", kwargs["user_id"])
    if not user:
        abort(404)

    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
               methods=["PUT"])
def reviews_update_review(review_id):
    """
    API route to update a review instance from the database under
    the id review_id
    """
    from api.v1.app import storage
    if not request.json:
        abort(400, description="Not a JSON")
    try:
        kwargs = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    for key, val in kwargs.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
