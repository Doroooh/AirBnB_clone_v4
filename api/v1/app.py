#!/usr/bin/python3
""" Flask Application """
""" This is the main application entry point to connect to the API """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

def create_app():
    """Creating and configuring Flask application"""
    app = Flask(__name__)
    app.register_blueprint(app_views)

    # Enabling Cross-Origin Resource Sharing (CORS)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    # Initializing Swagger for API documentation
    Swagger(app)

    @app.teardown_appcontext
    def close_storage(exception=None):
        """Close the storage on teardown"""
        storage.close()

    @app.errorhandler(404)
    def not_found_handler(error):
        """Handling errors"""
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.route('/api/v1/ui')
    @swag_from('swagger.yml')  # Swagger documentation for this route
    def api_ui():
        """Rendering API documentation UI"""
        return render_template('swaggerui.html')

    return app

if __name__ == "__main__":
    app = create_app()
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port)
