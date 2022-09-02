$(function() {
    var rowHeight = $('.row').outerHeight();
    var index = 0;
    $('.row:last-child').prependTo('.list');
    if($('.row').length >= 5) {
        $('.list').css('marginTop', -rowHeight);
    }

    function moveTop() {
        if($('.row').length < 5) {
            setTimeout(function(){;moveTop(); }, 5000);
            index = 0;
            return;
        }
        $('.list').animate({
            top: -rowHeight
        }, 2000, "linear", function() {
            index = index + 1;
            if(index === $('.row').length) {
                window.location.reload();
                index = 0;
            }
            $('.row:first-child').appendTo('.list');
            $('.list').css('top', '');
            moveTop();
        });
    }
    moveTop();
});
