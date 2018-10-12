# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for Promotion Demo Service
All of the models are stored in this module
Models
------
Promotion - The promotions used in the store for a sale
Attributes:
-----------
promo_name (string) - the name of the promotion
goods_name (string) - the name of the goods on promotion
category (string) - the category the promotion belongs to (i.e., home, kids)
price (double) - the price of the goods
dicount (double) - the discount percentage of tomorrow he promotion
available (boolean) - True for goods that are available for purchase

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Promotion(db.Model):
    """
    Class that represents a Promotion
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    promo_name = db.Column(db.String(63))
    goods_name = db.Column(db.String(63))
    category = db.Column(db.String(63))
    price = db.Column(db.Float())
    discount= db.Column(db.Float())
    available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Promotion %r>' % (self.name)

    def save(self):
        """
        Saves a Promotion to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Promotion from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Promotion into a dictionary """
        return {"id": self.id,
                "promo_name": self.promo_name,
                "goods_name": self.goods_name,
                "category": self.category,
                "price": self.price,
                "discount": self.discount,
                "available": self.available}

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary
        Args:
            data (dict): A dictionary containing the promotion data
        """
        try:
            self.promo_name = data['promo_name']
            self.goods_name = data['goods_name']
            self.category = data['category']
            self.price = data['price']
            self.discount = data['discount']
            self.available = data['available']
        except KeyError as error:
            raise DataValidationError('Invalid promotion goods: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid promotion goods: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Promotion.logger.info('Initializing database')
        Promotion.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Returns all of the Promotion goods in the database """
        Promotion.logger.info('Processing all Promotion goods')
        return Promotion.query.all()

    @staticmethod
    def find(promotion_id):
        """ Finds a Promotion good by it's ID """
        Promotion.logger.info('Processing lookup for id %s ...', promotion_id)
        return Promotion.query.get(promotion_id)

    @staticmethod
    def find_or_404(promotion_id):
        """ Find a Promotion goods by it's id """
        Promotion.logger.info('Processing lookup or 404 for id %s ...', promotion_id)
        return Promotion.query.get_or_404(promotion_id)

    @staticmethod
    def find_by_promo_name(promo_name):
        """ Returns all Promotion Goods with the given promotion name
        Args:
            name (string): the name of the Promotion you want to match
        """
        Promotion.logger.info('Processing promotion query for %s ...', promo_name)
        return Promotion.query.filter(Promotion.promo_name == promo_name)
    
    @staticmethod
    def find_by_goods_name(goods_name):
        """ Returns all Goods with the given name
        Args:
            name (string): the name of the goods you want to match
        """
        Promotion.logger.info('Processing goods query for %s ...', goods_name)
        return Promotion.query.filter(Promotion.goods_name == goods_name)

    @staticmethod
    def find_by_category(category):
        """ Returns all of the goods in a category
        Args:
            category (string): the category of the goods you want to match
        """
        Promotion.logger.info('Processing category query for %s ...', category)
        return Promotion.query.filter(Promotion.category == category)
   
    @staticmethod
    def find_by_availability(available=True):
        """ Query that finds goods by their availability """
        """ Returns all goods by their availability
        Args:
            available (boolean): True for goods that are available
        """
        Promotion.logger.info('Processing available query for %s ...', available)
        return Promotion.query.filter(Promotion.available == available)
