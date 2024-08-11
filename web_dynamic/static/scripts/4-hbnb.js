const $ = window.jQuery;

$(document).ready(function () {
  const amenities = {};
  $('input[type="checkbox"]').click(function () {
    $(this).each(function () {
      if (this.checked) {
        amenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete amenities[$(this).data('id')];
      }
    });
    $('.amenities h4').html(Object.values(amenities).join(', ') || '&nbsp;');
  });

  $('button').click(() => {
    const data = {
      amenities: Object.keys(amenities)
    };
    $('.places').empty();
    $.ajax({
      method: 'POST',
      url: 'http://localhost:5001/api/v1/places_search/',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8'
    })
      .done(function (data, status) {
        let placeTemplate;
        for (const place of data) {
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
  <div class="description">
    ${place.description}
  </div>
</article>
`;
          $('.places').append(placeTemplate);
        }
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

$.ajax({
  method: 'POST',
  url: 'http://localhost:5001/api/v1/places_search/',
  data: '{}',
  contentType: 'application/json; charset=utf-8'
})
  .done(function (data, status) {
    let placeTemplate;
    for (const place of data) {
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
      </article>
            `;
      $('.places').append(placeTemplate);
    }
  })
  .fail(function () {
    $('.places').hide();
  });
