"""
Promotion Model Test Suite

Test cases can be run with the following:
nosetests
coverage report -m
"""

import unittest
import time
import os
import json
from flask_api import status
from flask import Flask
from app import app, db
from app.models import Promotion, DataValidationError
import app.service as service

# DATABASE_URI = 'mysql+pymysql://root:passw0rd@localhost:3306/test'
DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(unittest.TestCase):
  """ Promotion Server Test """

  @classmethod
  def setUpClass(cls):
    app.debug = False
    # Set up the test database
    if DATABASE_URI:
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    service.init_db()
    db.drop_all()
    db.create_all()
    initial_data_1 = {
      'promo_name': 'Buy one get one free',
      'goods_name': 'Apple',
      'category': 'Fruit',
      'price': '2.99',
      'discount': '0.5',
      'available': False,
    }
    initial_data_2 = {
      'promo_name': '20% off',
      'goods_name': 'Carrot',
      'category': 'Vegetable',
      'price': '3.99',
      'discount': '0.8',
      'available': False,
    }
    initial_data_3 = {
      'promo_name': '70% off',
      'goods_name': 'IPhone XS',
      'category': 'Digital Products',
      'price': '1000.00',
      'discount': '0.7',
      'available': True,
    }
    self.save_promotion(initial_data_1)
    self.save_promotion(initial_data_2)
    self.save_promotion(initial_data_3)
    self.app = app.test_client()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_index(self):
    """ Test the Home Page """
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertIn('Promotion REST API Service', resp.data)

  def test_health(self):
    """ Test the server health checker """
    resp = self.app.get('/health')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(data['name'], 'Promotions REST API Service - Health')
    self.assertEqual(data['status'], 'OK')
    self.assertEqual(data['url'].split('/')[3], 'health')

  def test_list_promotions(self):
    """ Test of getting a list of all promotions """
    resp = self.app.get('/promotions')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(len(data), 3)

  def test_get_promotion(self):
    """ Test of getting a promotion with promotion id """
    promotion = Promotion.find_by_promo_name('Buy one get one free')[0]
    resp = self.app.get('/promotions/{}'.format(promotion.id))
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(data['promo_name'], promotion.promo_name)

  def test_get_promotion_not_found(self):
    """ Test of getting a nonexistent promotion """
    resp = self.app.get('/promotions/10')
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

  def test_create_promotion(self):
    """ Test of creating a new promotion """
    promotion_count = len(self.get_promotion())
    new_promotion = {
      'promo_name': '20% off',
      'goods_name': 'broccoli',
      'category': 'Vegetable',
      'price': '3.45',
      'discount': '0.8',
      'available': False,
    }
    data = json.dumps(new_promotion)
    resp = self.app.post('/promotions', data=data, content_type='application/json')
    self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    location = resp.headers.get('Location', None)
    self.assertTrue(location != None)
    resp_data = json.loads(resp.data)
    self.assertEqual(resp_data['promo_name'], '20% off')
    ## check if the new promotion has been added to the database
    new_promotions = self.get_promotion()
    self.assertIn(resp_data, new_promotions)
    self.assertEqual(len(new_promotions), promotion_count + 1)

  def test_create_promotion_invalid_type(self):
    """ Test of create a promotion without JSON type """
    new_promotion = {
      'promo_name': '20% off',
      'goods_name': 'broccoli',
      'category': 'Vegetable',
      'price': '3.45',
      'discount': '0.8',
      'available': True,
    }
    resp = self.app.post('/promotions', data=new_promotion, content_type='application/x-www-form-urlencoded')
    self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

  def test_update_promotion(self):
        """ Update an existing Promotion """
        promotion = Promotion.find_by_promo_name('Buy one get one free')[0]
        new_promo = dict(promo_name='Buy one get one free', goods_name='yogurt', category='Dairy', price=2.99,
      discount=0.5, available=True)
        data = json.dumps(new_promo)
        resp = self.app.put('/promotions/{}'.format(promotion.id),
                            data=data,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['category'], 'Dairy')

  def test_update_promotion_when_not_found(self):
      """ Try Updating a non existing Promotion """
      promotion = Promotion.find_by_promo_name('Buy one get one free')[0]
      new_promo = dict(promo_name='Buy one get one free', goods_name='yogurt', category='Dairy', price=2.99,
    discount=0.5, available=True)
      data = json.dumps(new_promo)
      resp = self.app.put('/promotions/{}'.format(promotion.id+10),
                          data=data,
                          content_type='application/json')
      self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_promotion(self):
     """ Delete a Promotion """
     promotion = Promotion.find_by_promo_name('Buy one get one free')[0]
     # save the current number of promotions for later comparison
     promotion_count = len(self.get_promotion())
     resp = self.app.delete('/promotions/{}'.format(promotion.id),
                               content_type='application/json')
     self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
     self.assertEqual(len(resp.data), 0)
     new_count = len(self.get_promotion())
     self.assertEqual(new_count, promotion_count - 1)

  def test_delete_unavailable_promotion(self):
    """ Delete all unavailable promotions """
    unavailable_promo_count = Promotion.find_by_availability(False).count()
    # initial count of unavailable promotions, make sure it's not empty
    self.assertNotEqual(unavailable_promo_count, 0)
    resp = self.app.delete('/promotions/unavailable')
    self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(len(resp.data), 0)
    new_unavailable_promo_count = Promotion.find_by_availability(False).count()
    self.assertEqual(new_unavailable_promo_count, 0)

  def test_query_promotion_list_by_name(self):
    """ Test of querying promotions by name """
    resp = self.app.get('/promotions', query_string='name=Buy20%+one20%+get20%+one20%+free')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertGreater(len(resp.data), 0)
    self.assertIn('Carrot', resp.data)
    self.assertNotIn('iPhone XS', resp.data)
    data = json.loads(resp.data)
    query_item = data[0]
    self.assertEqual(query_item['promo_name'], 'Buy one get one free')

  def test_query_promotion_list_by_availability(self):
    """ Test of querying promotions by availability """
    resp = self.app.get('/promotions', query_string='availability=False')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertGreater(len(resp.data), 0)
    self.assertIn('Carrot', resp.data)
    self.assertNotIn('IPhone XS', resp.data)
    data = json.loads(resp.data)
    query_item_1 = data[0]
    self.assertEqual(query_item_1['available'], False)
    query_item_2 = data[1]
    self.assertEqual(query_item_2['available'], False)

  def test_query_promotion_list_by_category(self):
    """ Test of querying promotions by category """
    resp = self.app.get('/promotions', query_string='category=Fruit')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertGreater(len(resp.data), 0)
    self.assertIn('Apple', resp.data)
    self.assertNotIn('IPhone XS', resp.data)
    data = json.loads(resp.data)
    query_item = data[0]
    self.assertEqual(query_item['category'], 'Fruit')

  def test_reset_promotion_data(self):
    """ Test of deleting all promotions """
    initial_count = len(self.get_promotion())
    self.assertNotEqual(initial_count, 0)
    resp = self.app.delete('/promotions/reset')
    self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(len(resp.data), 0)

  def test_method_not_allowed(self):
      """ Test method not allowed """
      resp = self.app.put('/promotions')
      self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  #def test_unsupported_media_type(self):
   #   """ Test method not allowed """
    #  resp = self.app.put('/promotions')
    #  self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

  def test_bad_request(self):
    """ Test Bad Request """
    new_promotion = {
      'promo_name': '20% off',
      'available': False,
    }
    data = json.dumps(new_promotion)
    resp = self.app.post('/promotions', data=data, content_type='application/json')
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

  def test_initialize_logging(self):
    """ Test the Logging Service """
    self.app = Flask(__name__)
    self.app.debug = False
    handler_list = list(self.app.logger.handlers)
    for log_handler in handler_list:
        self.app.logger.removeHandler(log_handler)
    service.initialize_logging()
    self.assertTrue(len(self.app.logger.handlers) == 1)
    service.initialize_logging()
    self.assertTrue(len(self.app.logger.handlers) == 1)

######################################################################
# Utility functions
######################################################################

  def get_promotion(self):
    """ get all current promotions """
    resp = self.app.get('/promotions')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    return data

  def save_promotion(self, data):
    """ save a promotion into the db """
    promotion = Promotion()
    promotion.deserialize(data)
    promotion.save()


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
  unittest.main()
