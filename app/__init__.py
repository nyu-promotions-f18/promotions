"""
Package: app
Package for the application models and services
"""
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)

import service
