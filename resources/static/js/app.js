$(function() {
    //on-close
    window.onbeforeunload = closing;
    function closing() {
        alert("leaving page")
        $("#stream").attr('src', '')
    }

    // number map function
    Number.prototype.map = function(in_min, in_max, out_min, out_max){
        if (this > in_max){ return out_max; }
        return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    }


    // get dream parameters
    def_layer = ""
    def_iteration = ""
    def_octave_n = ""
    def_octave_sc = ""
    def_step = ""

    function getDefaultValues() {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/default',
            success: function(response) {
                var obj = jQuery.parseJSON(response);
                console.log(obj)
                if (obj.layers != "" && obj.all_layers != "" && obj.default_layer != "") {
                    fillDefaultValues(obj.iteration, obj.layers, obj.all_layers, obj.default_layer, obj.layer);
                    fillAdvancedDefaultValues(obj.octave_n, obj.octave_scale, obj.step);
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

        function fillDefaultValues(iteration, fet_layers, all_layers, default_layer, layer) {
            def_layer = default_layer;
            def_iteration = iteration;

            $("#iteration").val(def_iteration);
            $("#layer").val(layer);
            $("#default").val(def_layer);

            $(fet_layers).each(function(index, item) {
                $("#dropdown-fet_layers").append('<div class="dropdown-item"><a> ' + item + '</a></div>');
            })

            $(all_layers).each(function(index, item) {
                $("#dropdown-all_layers").append('<div class="dropdown-item"><a> ' + item + '</a></div>');
            })

            $(".dropdown-layers").dropdown();
        }
        function fillAdvancedDefaultValues(octave_n, octave_scale, step){
            def_octave_n = octave_n;
            def_octave_sc = octave_scale;
            def_step = step;

            $("#octave_n").val(def_octave_n);
            $("#octave_scale").val(def_octave_sc);
            $("#step").val(def_step);
        }
        function initListeners() {
            $("#default").click(function() {
                $("#layer").val($.trim($(this).val()));

                $("#iteration").val(def_iteration);
                $("#default").val(def_layer);
                $("#octave_n").val(def_octave_n);
                $("#octave_scale").val(def_octave_sc);
                $("#step").val(def_step);
            });

            $(".dropdown-layers").on('click', '.dropdown-item a', function() {
                $("#layer").val($.trim($(this).text()));
            });
        }
    }
    getDefaultValues();


    // start dream; post parameters
    is_dreaming = false
    check_time_1 = 1000
    check_time_2 = 1000
    $("#start_dream").click(function() {
        startMusic()
        data = {
            iteration: $("#iteration").val(),
            layer: $("#layer").val(),
            octave_n: $("#octave_n").val(),
            octave_scale: $("#octave_scale").val(),
            step: $("#step").val()
        }

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: '/api/start_dream',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('success: ' + response)
                iteration = Number(data.iteration)
                check_time_1 = iteration.map(10, 100, 10000, 25000);
                check_time_2 = iteration.map(10, 100, 1000, 2500);
                checkIfDreaming(data.iteration)
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
                        // dream started
                        is_dreaming = true;
                        $(".overlay").css("opacity", "0.45");
                        setTimeout(checkIfDreaming, check_time_1);
                    }else{
                        setTimeout(checkIfDreaming, 1000);
                    }

                } else{
                    if(obj.is_dreaming == true){
                        setTimeout(checkIfDreaming, check_time_2);
                    }else{
                        // dream is done; stop music
                        stopMusic();
                        $(".overlay").css("opacity", "0");
                        is_dreaming = false;
                    }
                }
            },
            error: function(error) {
                console.log('error: ' + error)
                setTimeout(checkIfDreaming, check_time_2);
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
    $("#reset_dream").on("click", function() {
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



    $("#upload_dream").click(function() {
        print("uploading file")
    });
});
