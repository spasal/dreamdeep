$(function() {
    //on-close
    window.onbeforeunload = closing;

    function closing() {
        alert("leaving page")
        $("#cam_stream").attr('src', '')
    }

    // get data untill layers are not empty
    var received_layers = false;

    function getDefaultValues() {
        if (received_layers == false) {
            $.ajax({
                type: "GET",
                contentType: "application/json; charset=utf-8",
                url: '/api/default',
                success: function(response) {
                    var obj = jQuery.parseJSON(response);

                    if (obj.layers != "" && obj.all_layers != "" && obj.default_layer != "") {
                        received_layers = true
                        fillValues(obj.iteration, obj.layers, obj.all_layers, obj.default_layer);
                        initListeners();
                    } else {
                        console.log("layers are empty")
                        setTimeout(getDefaultValues, 500);
                    }
                },
                error: function(error) {
                    console.log('error: ' + error)
                    setTimeout(getDefaultValues, 500);
                }
            });

        }
    }
    setTimeout(getDefaultValues, 0);

    function fillValues(iteration, fet_layers, all_layers, default_layer) {
        $("#iteration").val(iteration);
        $("#layer").val(default_layer);
        $("#default").val(default_layer);

        $(fet_layers).each(function(index, item) {
            $("#dropdown-fet_layers").append('<div class="dropdown-item"><a> ' + item + '</a></div>');
        })

        $(all_layers).each(function(index, item) {
            $("#dropdown-all_layers").append('<div class="dropdown-item"><a> ' + item + '</a></div>');
        })

        $(".dropdown-layers").dropdown();
    }

    function initListeners() {
        $("#default").click(function() {
            $("#layer").val($.trim($(this).val()));
        });

        $(".dropdown-layers").on('click', '.dropdown-item a', function() {
            $("#layer").val($.trim($(this).text()));
        });
    }


    // post updates
    $("#start_dream").click(function() {
        console.log($("#iteration").val())
        data = {
            iteration: $("#iteration").val(),
            layer: $("#layer").val()
        }

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: '/api/start_dream',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('success: ' + response)
            },
            error: function(error) {
                console.log('error: ' + error)
            }
        });
    });

    $("#retry_dream").on("click", function() {
        console.log("clicked on get")
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/reset_view',
            success: function(response) {
                console.log('success: ' + response)
            },
            error: function(error) {
                console.log('error: ' + error)
            }
        });
    });

    $("#reset_vars").click(function() {

    });

    setTimeout(function() {
        console.log("test")
        $("#retry_dream").trigger('click')
    }, 1);
});