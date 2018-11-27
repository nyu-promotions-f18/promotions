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
price (float) - the price of the goods
dicount (float) - the discount percentage of the promotion
available (boolean) - True for promotions that are in use
"""
import os
import json
import logging
import ibm_db
from . import db

######################################################################
# Custom Exceptions
######################################################################
class DataValidationError(ValueError):
    pass

#class DatabaseConnectionError(ConnectionError):
#   pass

######################################################################
# Promotion Model for database
######################################################################
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
        # if the id is None it hasn't been added to the database
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
    def init_db():
        """ Initializes the database session """
        Promotion.logger.info('Initializing database')
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Returns all of the Promotion goods in the database """
        Promotion.logger.info('Processing all Promotion goods')
        return Promotion.query.all()
    
    @staticmethod
    def remove_all():
        """ Delete all promotions in the database """
        Promotion.logger.info('Deleting all promotions')
        Promotion.query.delete()
        db.session.commit()

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
    def find_by_category(category):
        """ Returns all of the goods in a category
        Args:
            category (string): the category of the goods you want to match
        """
        Promotion.logger.info('Processing category query for %s ...', category)
        return Promotion.query.filter(Promotion.category == category)

    @staticmethod
    def find_by_availability(available=True):
        """ Query that finds promotions by their availability """
        """ Returns all promotions by their availability
        Args:
            available (boolean): True for promotion that are in use
        """
        Promotion.logger.info('Processing available query for %s ...', available)
        return Promotion.query.filter(Promotion.available == available)
