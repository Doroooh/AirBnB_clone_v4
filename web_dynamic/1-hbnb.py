#!/usr/bin/python3
""" the code entry point for HBNB Flask Web Application"""
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

# Optional: Control Jinja2 template whitespace trimming
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

@app.teardown_appcontext
def close_db(exception=None):
    """Closing SQLAlchemy session after every request"""
    storage.close()

@app.route('/1-hbnb', strict_slashes=False)
def hbnb():
    """Rendering main HBNB page using the dynamically loaded data"""
    
    # Fetching state objects and sorting by name
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Pairing every state with cities, sorted by name
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Fetching and sorting all amenity objects by name
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Fetching and sorting all Place objects by name
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering '1-hbnb.html' template with sorted data and a cache id
    return render_template('1-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Starting Flask web application"""
    app.run(host='0.0.0.0', port=5000)
