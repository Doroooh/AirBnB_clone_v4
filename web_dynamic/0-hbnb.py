#!/usr/bin/python3
"""Launching the HBNB Flask Web Application"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, render_template
import uuid

app = Flask(__name__)

# Optional to trim and strip whitespace in Jinja2 templates
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

@app.teardown_appcontext
def close_db(exception=None):
    """ to close database connection when request ends"""
    storage.close()

@app.route('/0-hbnb', strict_slashes=False)
def hbnb():
    """ to render main HBNB page with dynamic content"""
    # Retrieving and sorting states by name
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    
    # Combining states with the respective sorted cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    # Amenities are retrieved and sorted by name
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    # Places are retrieved and sorted by name
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    # Rendering template with collected data and a unique cache ID
    return render_template('0-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """ Flask application runs """
    app.run(host='0.0.0.0', port=5000)
