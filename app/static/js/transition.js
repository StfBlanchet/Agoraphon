$(document).ready(function() {

  $('.search_process').submit(function(e) {
    var view = $('#waitZone');
    var temp = '<div class="wait">' +
    '<h2 class="highlights-md text-white text-center my-5">Collecte en cours...</h2>' +
    '<div class="spinner-border text-light text-center" role="status">' +
    '<span class="sr-only">Veuillez patienter...</span>' +
    '</div></div>';
    view.append(temp);
    window.scrollTo(0, 0);
    $.post('/topics').done(function(data) {
        view.hide();
    });
  });

    $('.analytics_process').submit(function(e) {
    var view = $('#waitZone');
    var temp = '<div class="wait">' +
    '<h2 class="highlights-md text-white text-center my-5">Traitement en cours...</h2>' +
    '<div class="spinner-border text-light text-center" role="status">' +
    '<span class="sr-only">Veuillez patienter...</span>' +
    '</div></div>';
    view.append(temp);
    window.scrollTo(0, 0);
    $.post('/analytics').done(function(data) {
        view.hide();
    });
  });

    $('.grab_process').submit(function(e) {
    var view = $('#waitZone');
    var temp = '<div class="wait">' +
    '<h2 class="highlights-md text-white text-center my-5">Collecte en cours...</h2>' +
    '<p>Cette opération peut durer plusieurs minutes.</p>' +
    '<div class="spinner-border text-light text-center" role="status">' +
    '<span class="sr-only">Veuillez patienter...</span>' +
    '</div></div>';
    view.append(temp);
    window.scrollTo(0, 0);
    $.post('/posts').done(function(data) {
        view.hide();
    });
  });

    $('.nlp_process').submit(function(e) {
    var view = $('#waitZone');
    var temp = '<div class="wait">' +
    '<h2 class="highlights-md text-white text-center my-5">Traitement en cours...</h2>' +
    '<p>Cette opération peut durer plusieurs minutes.</p>' +
    '<div class="spinner-border text-light text-center" role="status">' +
    '<span class="sr-only">Veuillez patienter...</span>' +
    '</div></div>';
    view.append(temp);
    window.scrollTo(0, 0);
    $.post('/nlp').done(function(data) {
        view.hide();
    });
  });

});

function hideIt() {
  $("#message").hide();
}
