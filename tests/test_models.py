"""
Promotion Model Test Suite

Test cases can be run with the following:
nosetests -v --with-spec --spec-color
coverage report -m
"""

import os
import unittest
from app import app, db
from app.models import Promotion, DataValidationError

# DATABASE_URI = 'mysql+pymysql://root:passw0rd@localhost:3306/test'
DATABASE_URI = os.getenv('DATABASE_URI', None)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotions(unittest.TestCase):
    """ Test Cases for Promotions """

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
        #Promotion.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_promotion(self):
        """ Create a promotion and assert that it exists """
        promotion = Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True)
        self.assertTrue(promotion != None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.promo_name, "random")
        self.assertEqual(promotion.goods_name, "random_good")
        self.assertEqual(promotion.category, "random_category")
        self.assertEqual(promotion.price, 20)
        self.assertEqual(promotion.discount, 20)
        self.assertEqual(promotion.available, True)

    def test_add_a_promotion(self):
        """ Create a promotion and add it to the database """
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True)
        self.assertTrue(promotion != None)
        self.assertEqual(promotion.id, None)
        promotion.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(promotion.id, 1)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_update_a_promotion(self):
        """ Update a promotion in the database """
        promotion = Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True)
        promotion.save()
        self.assertEqual(promotion.id,1)
        #change it and save it
        promotion.category = "random_afterchange"
        promotion.save()
        self.assertEqual(promotion.id,1)
        #Fetch it back to make sure the id not changed, but only the data           
        promotions = Promotion.all()
        self.assertEqual(len(promotions),1)
        self.assertEqual(promotions[0].category,"random_afterchange")

    def test_delete_a_promotion(self):
        """ Delete a promotion in the database """
        promotion = Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True)
        promotion.save()
        self.assertEqual(len(Promotion.all()),1)
        #delete the promotion
        promotion.delete()
        self.assertEqual(len(Promotion.all()),0)

    def test_serialize_a_pet(self):
        """ Test serialization of a Promotion """
        promotion = Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=False)        
        data = promotion.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('promo_name', data)
        self.assertEqual(data['promo_name'], "random")
        self.assertIn('goods_name', data)
        self.assertEqual(data['goods_name'], "random_good")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "random_category")
        self.assertIn('price', data)
        self.assertEqual(data['price'], 20)
        self.assertIn('discount', data)
        self.assertEqual(data['discount'], 20)
        self.assertIn('available', data)
        self.assertEqual(data['available'], False)

    def test_deserialize_a_pet(self):
        """ Test deserialization of a Promotion """
        data = {"id": 1, "promo_name": "random", "goods_name": "random_good", "category": "random_category", "price": 20, "discount": 20, "available": True}
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertNotEqual(promotion, None)
        self.assertEqual(promotion.id, None)
        self.assertEqual(promotion.promo_name, "random")
        self.assertEqual(promotion.goods_name, "random_good")
        self.assertEqual(promotion.category, "random_category")
        self.assertEqual(promotion.price, 20)
        self.assertEqual(promotion.discount, 20)
        self.assertEqual(promotion.available, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_find_promotion(self):
        """ Find a Promotion by ID """
        Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True).save()
        random2 = Promotion(promo_name="random2", goods_name="random2_good", category="random2_category", price=2, discount=2, available=False)
        random2.save()
        promotion = Promotion.find(random2.id)
        self.assertIsNot(promotion, None)
        self.assertEqual(promotion.id, random2.id)
        self.assertEqual(promotion.promo_name, "random2")
        self.assertEqual(promotion.goods_name, "random2_good")
        self.assertEqual(promotion.category, "random2_category")
        self.assertEqual(promotion.price, 2)
        self.assertEqual(promotion.discount, 2)
        self.assertEqual(promotion.available, False)

    def test_find_by_category(self):
        """ Find Promotion goods by Category """
        Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True).save()
        Promotion(promo_name="random2", goods_name="random2_good", category="random2_category", price=2, discount=2, available=False).save()
        promotions = Promotion.find_by_category("random2_category")
        self.assertEqual(promotions[0].category, "random2_category")
        self.assertEqual(promotions[0].promo_name, "random2")
        self.assertEqual(promotions[0].goods_name, "random2_good")
        self.assertEqual(promotions[0].price, 2)        
        self.assertEqual(promotions[0].discount, 2)
        self.assertEqual(promotions[0].available, False)

    def test_find_by_promo_name(self):
        """ Find all Promotion goods by promotions Name """
        Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True).save()
        Promotion(promo_name="random2", goods_name="random2_good", category="random2_category", price=2, discount=2, available=False).save()
        promotions = Promotion.find_by_promo_name("random2")
        self.assertEqual(promotions[0].category, "random2_category")
        self.assertEqual(promotions[0].promo_name, "random2")
        self.assertEqual(promotions[0].goods_name, "random2_good")
        self.assertEqual(promotions[0].price, 2)     
        self.assertEqual(promotions[0].discount, 2)
        self.assertEqual(promotions[0].available, False)

    def test_find_by_availability(self):
        """ Find all Promotion goods by availability """
        Promotion(promo_name="random", goods_name="random_good", category="random_category", price=20, discount=20, available=True).save()
        Promotion(promo_name="random2", goods_name="random2_good", category="random2_category", price=2, discount=2, available=False).save()
        promotions = Promotion.find_by_availability(False)
        self.assertEqual(promotions[0].category, "random2_category")
        self.assertEqual(promotions[0].promo_name, "random2")
        self.assertEqual(promotions[0].goods_name, "random2_good")
        self.assertEqual(promotions[0].price, 2)
        self.assertEqual(promotions[0].discount, 2)
        self.assertEqual(promotions[0].available, False)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestPets)
    # unittest.TextTestRunner(verbosity=2).run(suite)
