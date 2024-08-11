#!/usr/bin/python3
""" Blueprint for the E-Commerce API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing the various routes for e-commerce platforms

from api.v1.views.index import *  # the home and index routes
from api.v1.views.states import * # the category-specific routes
from api.v1.views.places import * # Product-specific routes
from api.v1.views.places_reviews import * # Routes for managing product reviews
from api.v1.views.cities import * # Routes for managing locations
from api.v1.views.amenities import * # Feature-specific routes (e.g., discounts, promotions)
from api.v1.views.users import * # Customer account management routes
from api.v1.views.places_amenities import * # Routes for managing product-specific features
