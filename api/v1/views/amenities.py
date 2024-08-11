#!/usr/bin/python3
""" Handles all default RESTful API actions for Product Features """
from models.product_feature import ProductFeature
from models import database_storage
from api.v2.controllers import shop_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@shop_views.route('/features', methods=['GET'], strict_slashes=False)
@swag_from('documentation/product_feature/all_features.yml')
def get_features():
    """
    Retrieves a list of all product features
    """
    all_features = database_storage.all(ProductFeature).values()
    list_features = []
    for feature in all_features:
        list_features.append(feature.to_dict())
    return jsonify({"status": "success", "features": list_features})


@shop_views.route('/features/<feature_id>/', methods=['GET'],
                  strict_slashes=False)
@swag_from('documentation/product_feature/get_feature.yml', methods=['GET'])
def get_feature(feature_id):
    """ Retrieves a specific product feature """
    feature = database_storage.get(ProductFeature, feature_id)
    if not feature:
        abort(404, description="Feature not found")

    return jsonify({"status": "success", "feature": feature.to_dict()})


@shop_views.route('/features/<feature_id>', methods=['DELETE'],
                  strict_slashes=False)
@swag_from('documentation/product_feature/delete_feature.yml', methods=['DELETE'])
def delete_feature(feature_id):
    """
    Deletes a product feature
    """

    feature = database_storage.get(ProductFeature, feature_id)

    if not feature:
        abort(404, description="Feature not found")

    database_storage.delete(feature)
    database_storage.save()

    return make_response(jsonify({"status": "success", "message": "Feature deleted"}), 200)


@shop_views.route('/features', methods=['POST'], strict_slashes=False)
@swag_from('documentation/product_feature/post_feature.yml', methods=['POST'])
def post_feature():
    """
    Creates a new product feature
    """
    if not request.get_json():
        abort(400, description="Request payload is not a valid JSON")

    if 'name' not in request.get_json():
        abort(400, description="Feature name is missing")

    data = request.get_json()
    instance = ProductFeature(**data)
    instance.save()
    return make_response(jsonify({"status": "success", "feature": instance.to_dict()}), 201)


@shop_views.route('/features/<feature_id>', methods=['PUT'],
                  strict_slashes=False)
@swag_from('documentation/product_feature/put_feature.yml', methods=['PUT'])
def put_feature(feature_id):
    """
    Updates a product feature
    """
    if not request.get_json():
        abort(400, description="Request payload is not a valid JSON")

    ignore = ['id', 'created_at', 'updated_at']

    feature = database_storage.get(ProductFeature, feature_id)

    if not feature:
        abort(404, description="Feature not found")

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(feature, key, value)
    database_storage.save()
    return make_response(jsonify({"status": "success", "feature": feature.to_dict()}), 200)
