var $grid = $('.grid').packery({
  // options
  itemSelector: '.grid-item',
  gutter: 10
});

function show_info(element) {
    var $this = $(element);
    $this.css('background-image', '');
    $this.children().first().removeClass('invisible');
}

function show_cover(element) {
    var $ele = $(element);
    var img = $ele.data('background-image');
    $ele.css('background-image', $ele.data('background-image'));
    $ele.children().first().addClass('invisible');
}

