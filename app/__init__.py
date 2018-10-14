"""
Package: app
Package for the application models and services.
Logging is enabled in this module to debug issues 
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)

# Load the confguration
app.config.from_object('config')
app.config['LOGGING_LEVEL'] = logging.INFO
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

# Set up the logging for production
print 'Setting up logging for {}...'.format(__name__)
app.logger.info('Logging established')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

from app import service, models
