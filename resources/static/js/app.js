$(function () {
  //on-close
  window.onbeforeunload = closing;
  function closing(){
    alert("leaving page")
    $("#cam_stream").attr('src','')
  }

  // get data untill layers are not empty
  var received_layers = false;
  function getDefaultValues(){
    if(received_layers == false){
      $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/default',
        success: function(response) {
          var obj = jQuery.parseJSON(response);

          if(obj.layers != ""){
            received_layers = true
            fillValues(obj.iteration, obj.layers, obj.all_layers)
          }else{
            console.log("layers are empty")
            setTimeout(getDefaultValues, 500);
          }
        },
        error: function(error){
          console.log('error: ' + error)
          setTimeout(getDefaultValues, 500);
        }
      });

    }
  }
  setTimeout(getDefaultValues, 0);

  function fillValues(iteration, fet_layers, all_layers){
    $("#iteration").val(iteration)

    $(fet_layers).each( function(index, item){
      $("#dropdown-fet_layers").append('<a class="dropdown-item az"> ' + item + '</a>');
    })

    $(all_layers).each( function(index, item){
      $("#dropdown-all_layers").append('<a class="dropdown-item az"> ' + item + '</a>');
    })
  }

  $(".dropdown-layers a").click(function() {
    console.log(this.id);
    console.log($(this).val())
  });

  $(".az").click(function() {
    console.log(this.id);
    console.log($(this).val())
  });

   
   // post updates
   $("#start_dream").click(function() {
    console.log($("#iteration").val())
   	data = {
   		iteration: $("#iteration").val(),
     	test2: "val2"
   	}

   	$.ajax({
   		type: "POST",
  		contentType: "application/json; charset=utf-8",
   		url: '/api/start_dream',
   		data: JSON.stringify(data),
   		success: function(response) {
   			console.log('success: ' + response)
   		},
   		error: function(error){
   			console.log('error: ' + error)
   		}
   	});

    $("#retry_dream").click(function(){
      console.log("clicked on get")
      $.ajax({
        type: "GET",
        contentType: "application/json; charset=utf-8",
        url: '/api/reset_view',
        success: function(response) {
          console.log('success: ' + response)
        },
        error: function(error){
          console.log('error: ' + error)
        }
      });
    });

    $("#reset_vars").click(function(){

    });
   });
});