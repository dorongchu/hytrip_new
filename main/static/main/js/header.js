$('#targets target').click(function( e ){
    e.preventDefault();
    var targetId = $(this).attr("href");
    var top = $(targetId).offset().top;
    $('html, body').stop().animate({scrollTop: top }, 1500);
});