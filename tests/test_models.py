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
        #Pet.init_db()
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


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestPets)
    # unittest.TextTestRunner(verbosity=2).run(suite)
