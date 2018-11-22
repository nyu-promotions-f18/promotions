"""
Package: app
Package for the application models and services.
This module also sets up the logging to be used with gunicorn
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ibm_db_sa

# Create Flask application
app = Flask(__name__)

# Load the confguration
app.config.from_object('config')
app.config['LOGGING_LEVEL'] = logging.INFO
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))


# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set up the logging for production
print 'Setting up logging for {}...'.format(__name__)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

app.logger.info('Logging established')
