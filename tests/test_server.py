"""
Promotion Model Test Suite

Test cases can be run with the following:
nosetests
coverage report -m
"""

import unittest
import os
import json
from flask_api import status
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
    initial_data = {
      'promo_name': 'Buy one get one free',
      'goods_name': 'Apple',
      'category': 'Fruit',
      'price': '2.99',
      'discount': '0.5',
      'available': True,
    }
    promotion = Promotion()
    promotion.deserialize(initial_data)
    promotion.save()
    self.app = app.test_client()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_index(self):
    """ Test the Home Page """
    resp = self.app.get('/')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(data['name'], 'Promotions REST API Service')
    self.assertEqual(data['version'], '1.0')
    self.assertEqual(data['resource'].split('/')[3], 'promotions')
    self.assertEqual(data['status'].split('/')[3], 'health')

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
    self.assertEqual(len(data), 1)

  def test_get_promotion(self):
    """ Test of getting a promotion with promotion id """
    promotion = Promotion.find_by_promo_name('Buy one get one free')[0]
    resp = self.app.get('/promotions/{}'.format(promotion.id))
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    data = json.loads(resp.data)
    self.assertEqual(data['promo_name'], promotion.promo_name)
  
  def test_get_promotion_not_found(self):
    """ Test of getting a nonexistent promotion """
    resp = self.app.get('/promotions/0')
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
      'available': True,
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

#  def test_delete_promotion(self):
#     """ Delete a Promotion """
#     promotion = Promotion.find_by_name('Buy one get one free')[0]
#     # save the current number of pets for later comparrison
#     pet_count = self.get_pet_count()
#     resp = self.app.delete('/pets/{}'.format(pet.id),
#                               content_type='application/json')
#     self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
#     self.ass:rtEqual(len(resp.data), 0)
#     new_count = self.get_pet_count()
#     self.assertEqual(new_count, pet_count - 1)    

######################################################################
# Utility functions
######################################################################

  def get_promotion(self):
      """ save the current number of promotions """
      resp = self.app.get('/promotions')
      self.assertEqual(resp.status_code, status.HTTP_200_OK)
      data = json.loads(resp.data)
      return data


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
  unittest.main()
