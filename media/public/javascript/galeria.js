$(document).ready(function() {
    $('body').on('click', 'div.close', function() {
        $(this).parents('div.background').remove();
    });
    $('body').on('click', 'div.gal-active', function(event) {
        event.preventDefault();
        var oid = $(this).attr('id');
        $.ajax({
            url: '/ver_galeria/',
            data: {'oid': oid},
            type: 'GET',
            success: function(data) {
                $('body').prepend(data);
                $('a.thumb-view:first').trigger('click');
            }
        });
    });
    $('body').on('click', 'a.thumb-view', function(event) {
        event.preventDefault();
        var oid = $(this).attr('id');
        var old = $('a.active-thumb').attr('id');
        $('#f-'+old).hide();
        $('a.active-thumb').removeClass('active-thumb');
        $('#f-'+oid).css('visibility', 'visible').fadeIn(100);
        $(this).addClass('active-thumb');
    });
    $('body').on('mouseenter', 'div#ver-foto', function() {
        $('img.prev').css('visibility', 'visible').fadeIn('fast');
        $('img.next').css('visibility', 'visible').fadeIn('fast');
        $('img.delf').css('visibility', 'visible').fadeIn('fast');
    });
    $('body').on('mouseleave', 'div#ver-foto', function() {
        $('img.prev').fadeOut('fast');
        $('img.next').fadeOut('fast');
        $('img.delf').fadeOut('fast');
    });
    $('body').on('click', 'img.prev', function() {
        var active = $('a.active-thumb').prev('a.thumb-view');
        active.trigger('click');
    });
    $('body').on('click', 'img.next', function() {
        var active = $('a.active-thumb').next('a.thumb-view');
        active.trigger('click');
    });
});