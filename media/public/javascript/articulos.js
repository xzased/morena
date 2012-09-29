$(document).ready(function() {
    $('a#agregar-articulo').on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: '/org/agregar_articulo',
            type: 'GET',
            success: function(data) {
                $('body').prepend(data);
                tinyMCE.init({
                    mode: 'exact',
                    elements : 'contenido',
                    width: '100%',
                    height: '340px'
                });
            }
        });
    });
    $('a#borrar-articulo').on('click', function(event) {
        event.preventDefault();
        var list = [];
        var items = $('.aselect:checked');
        $.each(items, function(i) {
            var a = $(this).attr('articulo');
            list.push(a);
        });
        $.ajax({
            url: '/org/borrar_articulo',
            type: 'POST',
            data: {'articulos': JSON.stringify(list)},
            success: function(data) {
                if (data.error) {
                    alert('Hubo un error al borrar los articulos.');
                } else {
                    $.each(items, function(i) {
                        $(this).parents('tr').remove();
                    });
                }
            }
        });
    });
    $('a#modificar-articulo').on('click', function(event) {
        event.preventDefault();
        var item = $('.aselect:checked');
        if (item.length > 1) {
            alert('Eh kiubo, a donde? Solo puedes elegir un articulo para modificar.');
            return false;
        } else if (item.length == 0) {
            alert('Eh kiubo, a donde? Tienes que elegir un articulo cana.');
            return false;
        } else {
            var oid = item.attr('articulo');
        }
        $.ajax({
            url: '/org/modificar_articulo',
            type: 'POST',
            data: {'articulo': oid},
            success: function(data) {
                $('body').prepend(data);
                tinyMCE.init({
                    mode: 'exact',
                    elements : 'contenido',
                    width: '100%',
                    height: '340px'
                });
            }
        });
    });
    $('body').on('click', 'div.close', function() {
        $(this).parents('div.background').remove();
    });
    $('body').on('submit', 'form#articulo', function(event) {
        event.preventDefault();
        var data = $(this).serialize();
        $.ajax({
            url: '/org/agregar_articulo',
            type: 'POST',
            data: data,
            dataType:'json',
            success: function(data) {
                $('div.close').trigger('click');
                $('#atable > tbody').prepend('<tr>\
                    <td> <input class="aselect" articulo="'+data._id+'" type="checkbox" /></td>\
                    <td>'+data.fecha+'</td><td>'+data.titulo+'</td><td>'+data.categoria+'</td>\
                    <td>'+data.orden+'</td><td>'+data.documentos+'</td></tr>');
            },
            error: function() {
                alert('Ha ocurrido un error, contacta al administrador \
                        y dile que en algo la cajeteo');
            }
        });
    });
  $('body').on('submit', 'form#mod-articulo', function(event) {
        event.preventDefault();
        var data = $(this).serialize();
        var item = $('.aselect:checked');
        $.ajax({
            url: '/org/guardar_articulo',
            type: 'POST',
            data: data,
            dataType:'json',
            success: function(data) {
                $('div.close').trigger('click');
                item.parents('tr').html('<td> <input class="aselect" articulo="'+data._id+'" type="checkbox" /></td>\
                    <td>'+data.fecha+'</td><td>'+data.titulo+'</td><td>'+data.categoria+'</td>\
                    <td>'+data.orden+'</td><td>'+data.documentos+'</td>');
            },
            error: function() {
                alert('Ha ocurrido un error, contacta al administrador \
                        y dile que en algo la cajeteo');
            }
        });
    });
});