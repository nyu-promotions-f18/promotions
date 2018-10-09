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
