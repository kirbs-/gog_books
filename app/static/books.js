var $grid = $('.grid').packery({
  // options
  itemSelector: '.grid-item',
  gutter: 10
});

//$grid.imagesLoaded().progress( function() {
//  $grid.packery();
//});

$(function () {
  $('[data-toggle="popover"]').popover({trigger: 'hover'})
})