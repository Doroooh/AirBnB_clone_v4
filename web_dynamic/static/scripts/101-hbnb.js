// Accessing jQuery from global window object
const $ = window.jQuery;

// Document ready function that ensures DOM is fully loaded before script execution
$(document).ready(function () {
  // Initializing objects for storing selected amenities, states, and cities
  const amenities = {};
  const states = {};
  const cities = {};

  // Event handler to click on amenity checkboxes
  $('input[type="checkbox"].amen-checkbox').click(function () {
    $(this).each(function () {
      // Adding or removing an amenity 
      if (this.checked) {
        amenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete amenities[$(this).data('id')];
      }
    });
    // Updating amenities list for display
    $('.amenities h4').html(Object.values(amenities).join(', ') || '&nbsp;');
  });

  // click on state checkboxes
  $('input[type="checkbox"].state-checkbox').click(function () {
    $(this).each(function () {
      // Add or remove state 
      if (this.checked) {
        states[$(this).data('id')] = $(this).data('name');
      } else {
        delete states[$(this).data('id')];
      }
    });
    // Update locations list 
    const locations = Object.values(states).concat(Object.values(cities));
    $('.locations h4').html(locations.join(', ') || '&nbsp;');
  });

  // click city checkboxes
  $('input[type="checkbox"].city-checkbox').click(function () {
    $(this).each(function () {
      // Add or remove city 
      if (this.checked) {
        cities[$(this).data('id')] = $(this).data('name');
      } else {
        delete cities[$(this).data('id')];
      }
    });
    // Update locations list 
    const locations = Object.values(states).concat(Object.values(cities));
    $('.locations h4').html(locations.join(', ') || '&nbsp;');
  });

  // click the search button
  $('button').click(() => {
    // Collect filters on the object
    const data = {
      amenities: Object.keys(amenities),
      states: Object.keys(states),
      cities: Object.keys(cities)
    };
    // clear places container before loading new data
    $('.places').empty();
    // Perform AJAX POST request that will fetch filtered places
    $.ajax({
      method: 'POST',
      url: 'http://localhost:5001/api/v1/places_search/',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8'
    })
      .done(function (data, status) {
        // handle received places data
        findPlaces(data);
      });
  });
});

// Perform GET request that check API status
$.get('http://localhost:5001/api/v1/status/')
  .done(function (data, status) {
    // Update API status indicator
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    }
  })
  .fail(function () {
    // Remove 'available' class if request fails
    $('#api_status').removeClass('available');
  });

// Function that retrieves and formats reviews
async function getReviews (reviews) {
  let reviewTemplate;
  let reviewsUL = '';
  let user;
  let formatDate;
  // Looping review and format
  for (const review of reviews) {
    user = await $.get(`http://localhost:5001/api/v1/users/${review.user_id}`);
    formatDate = new Date(review.updated_at).toLocaleDateString(
      'en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    reviewTemplate = `
      <li>
        <h3>From ${user.first_name} ${user.last_name} on ${formatDate}</h3>
        <p>${review.text}</p>
      </li>`;
    reviewsUL += reviewTemplate;
  }
  return reviewsUL;
}

// Function to find and display places based on search results
async function findPlaces (places) {
  let placeTemplate;
  let amenities;
  let amenityTemplate;
  let reviews;
  // Looping through place and create its template
  for (const place of places) {
    amenities = await $.get(`http://localhost:5001/api/v1/places/${place.id}/amenities`);
    reviews = await $.get(`http://localhost:5001/api/v1/places/${place.id}/reviews`);
    placeTemplate = `
    <article>
      <div class="title_box">
        <h2>${place.name}</h2>
        <div class="price_by_night">$${place.price_by_night}</div>
      </div>
      <div class="information">
        <div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>
        <div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>
        <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>
      </div>
      <!-- User div has been removed -->
      <div class="description">
        ${place.description}
      </div>
      <div class="amenities">
        <h2>Amenities</h2>
        <hr>
        <ul>
        </ul>
      </div>
      <div class="reviews">
        <h2>${reviews.length} Review${reviews.length !== 1 ? 's' : ''}</h2>
        <hr>
        <ul>
        </ul>
      </div>
    </article>
    `;
    // Append the place template to the places container
    $('.places').append(placeTemplate);
    // Add amenities to the place's amenities section
    for (const amenity of amenities) {
      amenityTemplate = `
        <li class="${amenity.name.toLowerCase().replace(' ', '_')}">${amenity.name}</li>
        `;
      $('.amenities:last ul').append(amenityTemplate);
    }
    // Add reviews to the place's reviews section
    $('.reviews:last ul').append(await getReviews(reviews));
  }
}

// Initial AJAX request to fetch all places and display them
$.ajax({
  method: 'POST',
  url: 'http://localhost:5001/api/v1/places_search/',
  data: '{}',
  contentType: 'application/json; charset=utf-8'
})
  .done(function (data, status) {
    // Call function that handle and displays the fetched places
    findPlaces(data);
  })
  .fail(function () {
    // Hiding places container if the request fails
    $('.places').hide();
  });
