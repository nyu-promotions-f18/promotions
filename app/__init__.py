"""
Package: app
Package for the application models and services
"""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)

# Load the confguration
app.config.from_object('config')
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

# Initialize SQLAlchemy
db = SQLAlchemy(app)

from app import service, models
