var $grid = $('.grid').packery({
  // options
  itemSelector: '.grid-item',
  gutter: 10
});

function show_info(element) {
    var $this = $(element);
    $this.css('background-image', '');
    $this.children().first().removeClass('invisible');
};

function show_cover(element) {
    var $ele = $(element);
    var img = $ele.data('background-image');
    $ele.css('background-image', $ele.data('background-image'));
    $ele.children().first().addClass('invisible');
};

$(window).scroll(function() {
    if($(window).scrollTop() == $(document).height() - $(window).height()) {
           // ajax call get data from server and append to the div
           load_books();
    }
});

function number_of_books_per_row(){
    return Math.trunc($(window).width()/230);
}



function load_books(){
    if(!window.books_loading){
        window.books_loading = true;
        var book_cnt = $('.grid-item').length;
        var sort_type = $('.sort-active').text();
        var size = number_of_books_per_row();
        $.ajax({
            url: '/fetch/' + book_cnt + '/' + sort_type + '/' + size,
            method: 'GET',
            success: function(data){
                $('#grid').append(data);
                window.books_loading = false;
            }
        })
    }
}

$(document).ready(function(){
    load_books();

    $('#sortby').change(function(e){
        $('#grid').empty();
        load_books();
    });

    $('.sort').click(function(){
        alert($(this).text());
    });
});



