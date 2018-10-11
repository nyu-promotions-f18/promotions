
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
from . import app

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Promotions REST API Service',
                   version='1.0',
                   url='http://localhost:5000/health'), HTTP_200_OK

######################################################################
# GET HEALTH
######################################################################
@app.route('/health')
def health():
    """ Return service health """
    return jsonify(name='Promotions REST API Service - Health',
                   status='OK',
                   url='http://localhost:5000/health'), HTTP_200_OK


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
    return make_response(jsonify(pet.serialize()), status.HTTP_200_OK)
