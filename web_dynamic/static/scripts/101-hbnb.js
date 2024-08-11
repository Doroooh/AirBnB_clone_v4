const $ = window.jQuery;

$(document).ready(function () {
  const amenities = {};
  const states = {};
  const cities = {};
  $('input[type="checkbox"].amen-checkbox').click(function () {
    $(this).each(function () {
      if (this.checked) {
        amenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete amenities[$(this).data('id')];
      }
    });
    $('.amenities h4').html(Object.values(amenities).join(', ') || '&nbsp;');
  });

  $('input[type="checkbox"].state-checkbox').click(function () {
    $(this).each(function () {
      if (this.checked) {
        states[$(this).data('id')] = $(this).data('name');
      } else {
        delete states[$(this).data('id')];
      }
    });
    const locations = Object.values(states).concat(Object.values(cities));
    $('.locations h4').html(locations.join(', ') || '&nbsp;');
  });

  $('input[type="checkbox"].city-checkbox').click(function () {
    $(this).each(function () {
      if (this.checked) {
        cities[$(this).data('id')] = $(this).data('name');
      } else {
        delete cities[$(this).data('id')];
      }
    });
    const locations = Object.values(states).concat(Object.values(cities));
    $('.locations h4').html(locations.join(', ') || '&nbsp;');
  });

  $('button').click(() => {
    const data = {
      amenities: Object.keys(amenities),
      states: Object.keys(states),
      cities: Object.keys(cities)
    };
    $('.places').empty();
    $.ajax({
      method: 'POST',
      url: 'http://localhost:5001/api/v1/places_search/',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8'
    })
      .done(function (data, status) {
        findPlaces(data);
      });
  });
});

$.get('http://localhost:5001/api/v1/status/')
  .done(function (data, status) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    }
  })
  .fail(function () {
    $('#api_status').removeClass('available');
  });

async function getReviews (reviews) {
  let reviewTemplate;
  let reviewsUL = '';
  let user;
  let formatDate;
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

async function findPlaces (places) {
  let placeTemplate;
  let amenities;
  let amenityTemplate;
  let reviews;
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
      <!-- user div removed -->
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
    $('.places').append(placeTemplate);
    for (const amenity of amenities) {
      amenityTemplate = `
        <li class="${amenity.name.toLowerCase().replace(' ', '_')}">${amenity.name}</li>
        `;
      $('.amenities:last ul').append(amenityTemplate);
    }
    $('.reviews:last ul').append(await getReviews(reviews));
  }
}

$.ajax({
  method: 'POST',
  url: 'http://localhost:5001/api/v1/places_search/',
  data: '{}',
  contentType: 'application/json; charset=utf-8'
})
  .done(function (data, status) {
    findPlaces(data);
  })
  .fail(function () {
    $('.places').hide();
  });
