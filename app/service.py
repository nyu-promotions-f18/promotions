
"""
Promotion Service

Paths:
------
GET /promotions - Returns a list all of the Pets
GET /promotions/{id} - Returns the Pet with a given id number
POST /promotions - creates a new Pet record in the database
PUT /promotions/{id} - updates a Pet record in the database
DELETE /promotions/{id} - deletes a Pet record in the database
"""

import os
import sys
from flask import Response, jsonify, request, json, url_for, make_response
from flask_api import status
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed, UnsupportedMediaType, InternalServerError # Exception Class
from . import app
from models import Promotion, DataValidationError

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message),status.HTTP_400_BAD_REQUEST

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), status.HTTP_404_NOT_FOUND

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), status.HTTP_500_INTERNAL_SERVER_ERROR

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Promotions REST API Service',
                   version='1.0',
                   resource=url_for('list_promotions', _external=True),
                   status=url_for('health', _external=True)), status.HTTP_200_OK

######################################################################
# GET HEALTH
######################################################################
@app.route('/health')
def health():
    """ Return service health """
    return jsonify(name='Promotions REST API Service - Health',
                   status='OK',
                   url=url_for('health', _external=True)),status.HTTP_200_OK

######################################################################
# LIST ALL PROMOTIONS
######################################################################
@app.route('/promotions', methods=['GET'])
def list_promotions():
    """ Returns all of the Promotions """
    promotions = []
    category = request.args.get('category')
    name = request.args.get('name')
    if category:
        promotions = Promotion.find_by_category(category)
    elif name:
        promotions = Promotion.find_by_goods_name(name)
    else:
        promotions = Promotion.all()

    results = [promotion.serialize() for promotion in promotions]
    return make_response(jsonify(results), status.HTTP_200_OK)



######################################################################
# RETRIEVE A PROMOTION
######################################################################
@app.route('/promotions/<int:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on it's id
    """
    promotion = Promotion.find(promotion_id)
    if not promotion:
        raise NotFound("Promotion with id '{}' was not found.".format(promotion_id))
    return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)
