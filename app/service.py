
"""
Promotion Service with Swagger

Paths:
------
GET /promotions - Returns a list all of the Promotions
GET /promotions/{id} - Returns the Promotion with a given id number
POST /promotions - creates a new Promotion record in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
DELETE /promotions/unavailable -deletes all promotions that are not available
"""

import os
import sys
import logging
from flask import Response, jsonify, request, json, url_for, make_response
from flask_api import status
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound,\
                        UnsupportedMediaType, InternalServerError # Exception Class

from . import app
from models import Promotion, DataValidationError  #, DatabaseConnectionError

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Promotions REST API Service',
          description='This is a Promotions REST API.',
          doc='/apidocs/'
          # prefix='/api'
         )

# This namespace is the start of the path i.e., /pets
ns = api.namespace('promotions', description='Promotion operations')

# Define the model so that the docs reflect what can be sent
promotion_model = api.model('Promotion', {
    'id': fields.Integer(readOnly=True,
                         description='The unique id assigned internally by service'),
    'promo_name': fields.String(required=True,
                          description='The name of the promotion'),
    'goods_name': fields.String(required=True,
                          description='The name of the goods on promotion'),
    'category': fields.String(required=True,
                              description='The category that the promotion belongs to'),
    'price': fields.Float(required=True,
                          description='Actual price of the goods on promotion'),
    'discount': fields.Float(required=True,
                          description='Price to be d'),
    'available': fields.Boolean(required=True,
                                description='Is the Promotion avaialble now?')
})

######################################################################
# Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = error.message or str(error)
    app.logger.info(message)
    return {'status':400, 'error': 'Bad Request', 'message': message}, 400
    #return bad_request(error)


#@api.errorhandler(DatabaseConnectionError)
#def database_connection_error(error):
#    """ Handles Database Errors from connection attempts """
#    message = error.message or str(error)
#    app.logger.critical(message)
#    return {'status':500, 'error': 'Server Error', 'message': message}, 500

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
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
@app.route('/health', methods=['GET'])
def health():
    """ Return service health """
    return jsonify(name='Promotions REST API Service - Health',
                   status='OK',
                   url=url_for('health', _external=True)),status.HTTP_200_OK


######################################################################
#  PATH: /promotions/{id}
######################################################################
@ns.route('/<int:promotion_id>')
@ns.param('promotion_id', 'The Promotion identifier')
class PromotionResource(Resource):
    """
    PromotionResource class
    Allows the manipulation of a single Promotion
    GET /promotion{id} - Returns a Promotion with the id
    PUT /promotion{id} - Update a Promotion with the id
    DELETE /promotion{id} -  Deletes a Promotion with the id
    """

    ######################################################################
    # RETRIEVE A PROMOTION
    ######################################################################
    @ns.doc('get_promotion with a given id')
    @ns.response(404, 'Promotion not found')
    @ns.marshal_with(promotion_model)
    def get(self,promotion_id):
        """
        Retrieve a single Promotion

        This endpoint will return a Promotion based on it's id
        """
        app.logger.info("Request to Retrieve a promotion with id [%s]", promotion_id)
        promotion = Promotion.find(promotion_id)
        if not promotion:
            raise NotFound("Promotion with id '{}' was not found.".format(promotion_id))
        return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)


    ######################################################################
    # UPDATE AN EXISTING PROMOTION
    ######################################################################
    @ns.doc('update_promotions')
    @ns.response(404, 'Promotion not found')
    @ns.response(400, 'The posted Promotion data was not valid')
    @ns.expect(promotion_model)
    @ns.marshal_with(promotion_model)
    def put(self,promotion_id):
        """
        Update a Promotion
        This endpoint will update a Promotion based the body that is posted
        """
        app.logger.info('Request to Update a promotion with id [%s]', pet_id)
        check_content_type('application/json')
        promotion = Promotion.find(promotion_id)
        if not promotion:
            raise NotFound("Promotion with id '{}' was not found.".format(promotion_id))

        data = api.payload
        app.logger.info(data)
        promotion.deserialize(data)
        promotion.id = promotion_id
        promotion.save()
        return make_response(jsonify(promotion.serialize()), status.HTTP_200_OK)




    ######################################################################
    # DELETE A PROMOTION
    ######################################################################
    @ns.doc('delete_promotion')
    @ns.response(204, 'Promotion deleted')
    def delete(self,promotion_id):
        """
        Delete a Promotion
        This endpoint will delete a Promotion based the id specified in the path
        """
        app.logger.info('Request to Delete a promotion with id [%s]', pet_id)
        promotion = Promotion.find(promotion_id)
        if promotion:
            promotion.delete()
        return make_response('', status.HTTP_204_NO_CONTENT)



######################################################################
#  PATH: /promotions
######################################################################
@ns.route('/', strict_slashes=False)
class PromotionCollection(Resource):
    """ Handles all interactions with collections of Promotion"""

    ######################################################################
    # LIST ALL PROMOTIONS
    ######################################################################
    @ns.doc('list_promotions')
    @ns.response(404, 'Promotion not found')
    @ns.marshal_with(promotion_model)
    def get(self):
        """ Returns all of the Promotions"""
        app.logger.info("Request to list all promotions")
        promotions = []
        category = request.args.get('category')
        name = request.args.get('name')
        availability = request.args.get('availability')
        if category:
            promotions = Promotion.find_by_category(category)
        elif name:
            promotions = Promotion.find_by_promo_name(name)
        elif availability:
            promotions = Promotion.find_by_availability(availability)
        else:
            promotions = Promotion.all()

        results = [promotion.serialize() for promotion in promotions]
        return make_response(jsonify(results), status.HTTP_200_OK)


    ######################################################################
    # CREATE A PROMOTION
    ######################################################################
    @ns.doc('create_promotions')
    @ns.expect(promotion_model)
    @ns.response(400, 'The posted data was not valid')
    @ns.response(201, 'Promotion created successfully')
    @ns.marshal_with(promotion_model, code=201)
    def post(self):
        """
        Create a new promotion
        This endpoint will create a promotion based on the data in the request body and save it into the db
        """
        app.logger.info('Request to Create a Promotion')
        check_content_type('application/json')
        promotion = Promotion()
        app.logger.info('Payload = %s', api.payload)
        promotion.deserialize(api.payload)
        promotion.save()
        app.logger.info('Promotion with new id [%s] saved!', promotion.id)
        location_url = api.url_for(PromotionResource, promotion_id=promotion.id, _external=True)
        saved_info = promotion.serialize()
        location_url = url_for('get_promotion', promotion_id = promotion.id, _external=True)
        return make_response(jsonify(saved_info), status.HTTP_201_CREATED, { 'Location': location_url })



######################################################################
#  PATH: /promotions/unavailable
######################################################################
@ns.route('/unavailable')
class UnavailableResource(Resource):
    """ Make a promotion unavailable """

    #######################################################
    # DELETE UNAVILABLE PROMOTIONS
    #######################################################
    @ns.doc('promotions_unavailable')
    @ns.response(404, 'Promotion not found')
    @ns.response(204, 'Unavailabe promotions deleted')
    def delete(self):
        """ Delete all unavailable Promotions

        This endpoint will delete all unavailable Promotions
        """
        promotions = Promotion.find_by_availability(False)
        if promotions:
            for promotion in promotions:
                promotion.delete()
            return make_response('', status.HTTP_204_NO_CONTENT)



######################################################################
# DELETE ALL PROMOTIONS DATA (for testing only)
######################################################################
@app.route('/promotions/reset', methods=['DELETE'])
def promotions_reset():
    """ Removes all promotions from the database """
    Promotion.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    Promotion.init_db()

def check_content_type(content_type):
    """ Validate the content type of request """
    if (request.headers['Content-Type'] == content_type):
        return
    app.logger.error('Invalid Content_Type: %s', request.headers['Content-Type'])
    raise UnsupportedMediaType('Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')
