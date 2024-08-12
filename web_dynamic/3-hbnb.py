#!/usr/bin/python3
""" the Flask Web Application:The HBNB Startup Script"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

# Initializing Flask application
app = Flask(__name__)

# Optional: Configure Jinja2 environment to handle template blocks more efficiently
# app.jinja_env.trim_blocks = True  # Trims spaces after block statements
# app.jinja_env.lstrip_blocks = True  # Removes leading spaces from block statements

@app.teardown_appcontext
def close_db(error):
    """Closing current SQLAlchemy session after every request"""
    storage.close()

@app.route('/3-hbnb', strict_slashes=False)
def hbnb():
    """Renders the HBNB page with data from the storage engine"""
    
    # Retrieving all State objects, sort by name in an alphabetic order 
    
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Pairing every state with cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Retrieving and sorting the Amenity objects in alphabetic order 
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Retrieving and sorting the place objects in alphabetic order 
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering '3-hbnb.html' template
    # Pass the sorted data and the unique cache ID
    return render_template('3-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Main entry point for running the Flask web application"""
    app.run(host='0.0.0.0', port=5000)
