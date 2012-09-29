$(document).ready(function() {
    $('a#agregar-galeria').on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: '/org/agregar_galeria',
            type: 'GET',
            success: function(data) {
                $('body').prepend(data);
            }
        });
    });
    $('a#borrar-galeria').on('click', function(event) {
        event.preventDefault();
        var list = [];
        var items = $('input.gal-checker:checked');
        $.each(items, function(i) {
            var a = $(this).attr('id');
            list.push(a);
        });
        $.ajax({
            url: '/org/borrar_galeria',
            type: 'POST',
            data: {'galerias': JSON.stringify(list)},
            success: function(data) {
                if (data.error) {
                    alert('Hubo un error al borrar la galeria(s) seleccionadas.');
                } else {
                    $.each(items, function(i) {
                        $(this).parents('div.gal').remove();
                    });
                }
            }
        });
    });
    $('a#subir-foto').on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: '/org/subir_foto',
            type: 'GET',
            success: function(data) {
                $('body').prepend(data);
            }
        });
    });
    $('body').on('click', 'div.close', function() {
        $(this).parents('div.background').remove();
    });
    $('body').on('submit', 'form#galeria', function(event) {
        event.preventDefault();
        var data = $(this).serialize();
        $.ajax({
            url: '/org/agregar_galeria',
            type: 'POST',
            data: data,
            dataType:'json',
            success: function(data) {
                $('div.close').trigger('click');
                $('#galerias').prepend('<div id="'+data._id+'" class="gal">\
                     <input type="checkbox" class="gal-checker" id="'+data._id+'"/>\
                    <h3>'+data.nombre.toUpperCase()+'</h3> <span class="sub"> creada justo ahora por \
                    '+data.usuario+'</span><div class="thumbs">\
                    <img class="unknown thumb" class="thumb" src="/static/images/unknown.jpg" /></div></div>');
            },
            error: function() {
                alert('Ha ocurrido un error, hay una galeria con el mismo nombre\
                        o no indicaste un nombre del todo');
            }
        });
    });
    $('body').on('submit', 'form#upload', function(event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: '/org/subir_foto',
            data: formData,
            type: 'POST',
            processData: false,
            contentType: false,
            cache: false,
            beforeSend: function() {
                $('#upload').html('<img id="loader" src="/org/static/images/ajax-big-loader.gif" />');
            },
            success: function(data) {
                var d = JSON.parse(data);
                $('div#'+d.galeria_id).addClass('gal-active');
                if ($('div#'+d.galeria_id).find('img.unknown').length > 0) {
                    $('div#'+d.galeria_id).find('img.unknown').remove();
                }
                $('div#'+d.galeria_id).find('div.thumbs').append('<img class="thumb" src="'+d['thumb-url']+'"/>');
                $('div.close').trigger('click');
            },
            error: function() {
                $('div.close').trigger('click');
                alert("Hubo un error al subir el archivo, checka que la imagen este en un formato aceptable ('jpeg', 'png', etc...)");
            }
        });
    });
    $('body').on('click', 'div.gal-active', function(event) {
        event.preventDefault();
        var oid = $(this).attr('id');
        $.ajax({
            url: '/org/ver_galeria/',
            data: {'oid': oid},
            type: 'GET',
            success: function(data) {
                $('body').prepend(data);
                $('a.thumb-view:first').trigger('click');
            }
        });
    });
    $('body').on('click', 'input.gal-checker', function(event) {
        event.stopPropagation();
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
    $('body').on('click', 'img.delf', function() {
        var oid = $('a.active-thumb').attr('id');
        var active = $('a.active-thumb');
        $.ajax({
            url: '/org/borrar_foto/',
            data: {'oid': oid},
            type: 'POST',
            success: function(data) {
                var t = active.next('a.thumb-view');
                if (t.length > 0) {
                    t.trigger('click');
                } else {
                    t = active.prev('a.thumb-view');
                    t.trigger('click');
                }
                active.remove();
                $('#f-'+oid).remove();
            },
            error: function() {
                alert("hubo un error al borrar la foto.");
            }
        });
    });
});