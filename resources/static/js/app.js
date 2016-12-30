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
        startMusic()
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
                check_time = 750;

                if (is_dreaming == false){
                    if(obj.is_dreaming == true){
                        // dream started
                        is_dreaming = true;
                    }
                    setTimeout(checkIfDreaming, check_time);
                } else{
                    if(obj.is_dreaming == true){
                        setTimeout(checkIfDreaming, check_time);
                    }else{
                        // dream is done; stop music
                        stopMusic();
                        is_dreaming = false;
                    }
                }
            },
            error: function(error) {
                console.log('error: ' + error)
                setTimeout(checkIfDreaming, check_time);
            }
        });
    }

    function startMusic(){
        console.log("start music");
        play_audio("play");
    }
    function stopMusic(){
        console.log("stop music");
        play_audio("stop");
    }
    function play_audio(task) {
        audioPlayer = $("#sweet_dreams");

        if(task == 'play'){
            audioPlayer.prop("volume",0);
            audioPlayer.trigger('play');
            audioPlayer.animate({volume: 0.5}, 3000);
        }
        if(task == 'stop'){
            audioPlayer.animate({volume: 0}, 3500, function(){
                audioPlayer.trigger('pause');
                audioPlayer.prop("currentTime",0);
            });
        }
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
        $("#reset_dream").trigger('click')
    }, 1);

    // file upload
    $("#upload_dream").click(function() {

    });
});
