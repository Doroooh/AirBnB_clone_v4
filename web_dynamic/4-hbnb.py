#!/usr/bin/python3
""" the Flask Web Application Entry Point: the HBNB"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

# Creating the Flask application instance
app = Flask(__name__)

# Optional: Modify Jinja2 template handling for whitespace
# app.jinja_env.trim_blocks = True  # Trims blocks in templates
# app.jinja_env.lstrip_blocks = True  # Strips leading spaces from blocks

@app.teardown_appcontext
def close_db(error):
    """Tearing down the present SQLAlchemy Session"""
    storage.close()

@app.route('/4-hbnb', strict_slashes=False)
def hbnb():
    """Rendering main HBNB page using dynamic data"""
    
    # Retrieveing all state objects, and sorting by name in alphabetic order
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Preparing the list of states paired with the respective sorted cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Retrieving and sorting by name all the Amenity objects 
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Retrieving and sorting by name the Place objects 
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering '4-hbnb.html' template, pass sorted data
    return render_template('4-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Starting Flask web application"""
    app.run(host='0.0.0.0', port=5000)
