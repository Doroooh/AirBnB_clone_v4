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

# Instantiating Flask application
app = Flask(__name__)

# Optional: Configure Jinja2 environment settings for template processing
# app.jinja_env.trim_blocks = True  # Trims extra spaces around Jinja2 blocks
# app.jinja_env.lstrip_blocks = True  # Removes leading whitespace in Jinja2 blocks

@app.teardown_appcontext
def close_db(error):
    """Closing current SQLAlchemy session after request completion"""
    storage.close()

@app.route('/2-hbnb', strict_slashes=False)
def hbnb():
    """Rendering HBNB page, loading data from storage engine"""
    
    # From storage retrieved and sorted by name the state objects from storage
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Createing a list to pair every with sorted cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Retrieving and sorting by name the Amenity objects 
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Retrieving and sorting by name all Place objects 
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering the '2-hbnb.html' ith sorted data and unique cache ID
    return render_template('2-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Main entry point to run Flask application"""
    app.run(host='0.0.0.0', port=5000)
