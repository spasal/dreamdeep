$(function() {
    //on-close
    window.onbeforeunload = closing;
    function closing() {
        alert("leaving page")
        $("#cam_stream").attr('src', '')
    }


    // get dream parameters
    function getDefaultValues() {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/default',
            success: function(response) {
                var obj = jQuery.parseJSON(response);

                if (obj.layers != "" && obj.all_layers != "" && obj.default_layer != "") {
                    fillDefaultValues(obj.iteration, obj.layers, obj.all_layers, obj.default_layer);
                    initListeners();
                } else {
                    setTimeout(getDefaultValues, 500);
                }
            },
            error: function(error) {
                console.log('error: ' + error)
                setTimeout(getDefaultValues, 500);
            }
        });
    }
    setTimeout(getDefaultValues, 0);

    function fillDefaultValues(iteration, fet_layers, all_layers, default_layer) {
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


    // start dream post parameters
    is_dreaming = false
    $("#start_dream").click(function() {
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
                checkIfDreaming()
            },
            error: function(error) {
                console.log('error: ' + error)
            }
        });
    });
    function checkIfDreaming(){
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/is_dream',
            success: function(response) {
                var obj = jQuery.parseJSON(response);

                if (is_dreaming == false){
                    if(obj.is_dreaming == true){
                        // dream started; start music
                        console.log("dream started")
                        is_dreaming = true
                    }else{
                        // dream not started
                        console.log("dream not yet started")
                    }
                    setTimeout(checkIfDreaming, 500);
                } else{
                    if(obj.is_dreaming == true){
                        // still dreaming; retry
                        console.log("still dreaming")
                        setTimeout(checkIfDreaming, 500);
                    }else{
                        // dream is done; stop music
                        console.log("dream done")
                        is_dreaming = false
                    }
                }
            },
            error: function(error) {
                console.log('error: ' + error)
                setTimeout(checkIfDreaming, 500);
            }
        });
    }


    // reset view + onpage_load click on button
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
    setTimeout(function() {
        $("#retry_dream").trigger('click')
    }, 1);

    // file upload
    $("#reset_vars").click(function() {

    });
});
