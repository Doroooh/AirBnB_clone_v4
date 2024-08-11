#!/usr/bin/python3
""" Customized Flask Application for Local Experiences Booking """

from experience_models import experience_storage
from api.v1.experience_views import experience_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

# Creating a new Flask application instance
app = Flask(__name__)

# Configuring the application
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['EXPERIENCE_API_TITLE'] = 'Local Experience Booking API'
app.config['SWAGGER'] = {
    'title': app.config['EXPERIENCE_API_TITLE'],
    'uiversion': 3
}

# Registering the API blueprint
app.register_blueprint(experience_views)

# Enabling CORS for API endpoints
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Defining the custom error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """ 404 Error - Experience Not Found
    ---
    responses:
      404:
        description: The requested experience was not found
    """
    return make_response(jsonify({'error': "Experience not found"}), 404)

# Defining the custom teardown function to close the database connection
@app.teardown_appcontext
def close_experience_db(error):
    """ Close Experience Storage """
    experience_storage.close()

# Initializing Swagger for API documentation
Swagger(app)

# Running application
if __name__ == "__main__":
    """ Main Function """
    host = environ.get('EXPERIENCE_API_HOST', '0.0.0.0')
    port = environ.get('EXPERIENCE_API_PORT', '8000')
    app.run(host=host, port=port, threaded=True)
