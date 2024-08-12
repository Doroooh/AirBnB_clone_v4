#!/usr/bin/python3
"""Flask Web Application: HBNB Initialization Script"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

# Initializing the Flask application 
app = Flask(__name__)

# Optional Jinja2 configuration to control whitespace in templates
# app.jinja_env.trim_blocks = True  # Strip newline after block
# app.jinja_env.lstrip_blocks = True  # Remove leading spaces before block

@app.teardown_appcontext
def close_db(error):
    """The teardown method. It will close current SQLAlchemy session"""
    storage.close()

@app.route('/100-hbnb', strict_slashes=False)
def hbnb():
    """ The View function renders HBNB page with dynamic data"""
    
    # Fetching and alphabetically sorting by name all State objects 
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Pairing every state with associated cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Fetching and sorting all Amenity objects 
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Fetching and sorting all Place objects 
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering '100-hbnb.html' template 
    return render_template('100-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Main entry point to run the Flask web server"""
    app.run(host='0.0.0.0', port=5000)
