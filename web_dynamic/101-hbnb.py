#!/usr/bin/python3
""" Flask Web Application: HBNB Initialization """
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

# Optional: Configure Jinja2 to optimize template rendering
# app.jinja_env.trim_blocks = True  # Removes newline after Jinja blocks
# app.jinja_env.lstrip_blocks = True  # Removes leading spaces before Jinja blocks

@app.teardown_appcontext
def close_db(error):
    """Closing current SQLAlchemy session after every request"""
    storage.close()

@app.route('/101-hbnb', strict_slashes=False)
def hbnb():
    """Rendering HBNB page using dynamic data from storage"""
    
    # Retrieving and name sorting alphabetically the State objects
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    
    # Pairing every state with corresponding cities
    st_ct = []
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda city: city.name)])

    # Retrieving and name sorting all Amenity objects 
    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    # Retrieving and sorting by name the Place objects
    places = storage.all(Place).values()
    places = sorted(places, key=lambda place: place.name)

    # Rendering '101-hbnb.html' template with sorted data and cache ID
    return render_template('101-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Starting Flask web server"""
    app.run(host='0.0.0.0', port=5000)
