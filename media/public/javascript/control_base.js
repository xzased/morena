$(document).ready(function() {
    $('a#logout').on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: '/org/logout',
            type: 'POST',
            success: function(data) {
                window.location = '/';
            }
        });
    });
});