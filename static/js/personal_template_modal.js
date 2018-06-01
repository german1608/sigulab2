$(document).ready(function () {
    $('.registration-form fieldset:first-child').fadeIn('slow');

    $('.registration-form input[type="text"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form input[type="checkbox"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form select[type="select"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('#sel2').change(function (){
        if ($("#sel2 option:selected").val()=="Fijo") {
            $("#fsalida").hide();
        }
        else {
            $("#fsalida").show();
        };
    });

    //-------------------------------- Primera parte del form agregar -----------------------------------------//

    // Manejo de error de la cedula
    $('[name="ci_add"]').change(function (){
        console.log($(this).val());
        if (!($(this).val().match(/^\d+$/gm)) || $(this).val()>99999999) { // CI
            
            $("#err_ci").html("Introduzca una cédula de identidad válida (Entre 1 y 99999999)");
            $("#err_ci").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            $(this).removeClass('input-error');
            $("#err_ci").hide();
        }
    });

    // Manejo de error del numero de celular 
    $('[name="celular_add"]').change(function (){
        if (!($(this).val().match(/^\d+$/gm))) { // Extension de 1 a 4 digitos
            $("#err_celular").html('El celular debe tener solo números');
            $("#err_celular").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else if ($(this).val()<999999){
            $(this).removeClass('input-error');
            $("#err_celular").hide();
            $("#err_celular").html('El celular tiene que tener el siguiente formato XXXXXXX');
            $("#err_celular").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            $(this).removeClass('input-error');
            $("#err_celular").hide();
        }
    });

    // Manejo de error del numero de residencia 
    $('[name="telefono_add"]').change(function (){
        if (!($(this).val().match(/^\d+$/gm))) { // Extension de 1 a 4 digitos
            $("#err_telefono").html('El telefono debe tener solo números');
            $("#err_telefono").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else if ($(this).val()<999999999){
            $(this).removeClass('input-error');
            $("#err_telefono").hide();
            $("#err_telefono").html('Tiene que tener el siguiente formato (codigoArea) XXXXXXX');
            $("#err_telefono").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            $(this).removeClass('input-error');
            $("#err_telefono").hide();
        }
    })


    // Manejo de error del campo de contacto de emergencia 
    $('[name="contacto_emergencia_add"]').change(function (){
        if (!($(this).val().match(/^\d+$/gm))) { // Extension de 1 a 4 digitos
            $("#err_emergencia").html('El contacto de emergencia debe tener solo números');
            $("#err_emergencia").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else if ($(this).val()<999999999){
            $(this).removeClass('input-error');
            $("#err_emergencia").hide();
            $("#err_emergencia").html('Tiene que tener el siguiente formato (codigoArea) XXXXXXX');
            $("#err_emergencia").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            $(this).removeClass('input-error');
            $("#err_emergencia").hide();
        }
    })

    // Manejo de error del campo de pagina de web 
    $('[name="pagina_web_add"]').change(function (){
        if (!($(this).val().match(/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$/))) { // Extension de 1 a 4 digitos
            $("#err_pagina_web").html("Formato incorrecto de pagina web");
            $("#err_pagina_web").show();
            $(this).addClass('input-error');
            next_step = false;
        }
        else {
            $(this).removeClass('input-error');
            $("#err_pagina_web").hide();
        }
    })

    // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;
        if (parent_fieldset.attr('id') === 'p1') {
            $(`[name="apellido_add"],
                [name="ci_add"],
                [name="email_add"],
                [name="telefono_add"],
                [name="celular_add"],
                [name="contacto_emergencia_add"],
                [name="direccion_add"],
                [name="pagina_web_add"]`).filter(function () {
                    $(this).next().first().hide()
                    $(this).removeClass('input-error')
                    return $(this).val() === ''
                }).each(function(idx) {
                    $(this).next().first().html('Por favor, llene el campo')
                    $(this).next().first().show()
                    $(this).addClass('input-error')
                    next_step = false
                })
        } else if (parent_fieldset.attr('id') === 'p2') {
            // dropdowns
            $(`[name="estatus_add"],
                [name="categoria_add"],
                [name="condicion_add"]`).filter(function () {
                    $(this).next().first().hide()
                    $(this).removeClass('input-error')
                    return $(this).val() === '' || $(this).val() === null
                }).each(function(idx) {
                    $(this).next().first().html('Por favor, escoja una opción')
                    $(this).next().first().show()
                    $(this).addClass('input-error')
                    next_step = false
                })

            // date inputs

            $(`[name="fecha_ingreso_usb_add"],
            [name="fecha_ingreso_ulab_add"],
            [name="fecha_ingreso_admin_publica_add"]`).filter(function () {
                console.log($(this).val())
                return $(this).val() === '' || $(this).val() === null
            }).each(function(idx) {
                $(this).addClass('input-error')
                next_step = false
            })
        }

        if (next_step) {
            parent_fieldset.fadeOut(400, function () {
                $(this).next().fadeIn();
            });
        }

    });

    // previous step
    $('.registration-form .btn-previous').on('click', function () {
        $(this).parents('fieldset').fadeOut(400, function () {
            $(this).prev().fadeIn();
        });
    });


    
    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');

        parent_fieldset.find('input[type="text"]').each(function () {
            // if (($(this).val() == "") && ($(this).attr('required'))) {
            //     if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
            //         $("#err_cargo").html("Este campo es obligatorio");
            //         $("#err_cargo").show();
            //     }
            //     $(this).addClass('input-error');
            //     e.preventDefault();
            // } else {
            //     if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
            //         if (!($(this).val().match(/^(([a-zA-Z ]+[\-\'\.]?)+[a-zA-Z ]+)+$/))) { // Todo lo que sea nombres (Antes del submit)
            //             $("#err_cargo").html("Introduzca un cargo válido");
            //             $("#err_cargo").show();
            //             $(this).addClass('input-error');
            //             e.preventDefault();
            //         }
            //         else {
            //             $("#err_cargo").hide();
            //             $(this).removeClass('input-error');
            //         }
            //     }
            //     else {
            //         $(this).removeClass('input-error');
            //     }
            // }
        });

    });
    
    


   
});
