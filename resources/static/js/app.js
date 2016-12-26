$(function () {
  // get data untill layers are not empty
  var received_layers = false;
  console.log("before while")
  while(received_layers == false){
    setTimeout(function() {
         // load default values
         $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: '/api/default',
            success: function(response) {
              var obj = jQuery.parseJSON(response);

              $("#iteration").val(obj.iteration)
              $("#fet_layers").val(obj.layers)

              console.log(obj.layers)

              if(obj.layers != ""){
                console.log("layers are not ''")
                received_layers = true
              }else{
                console.log("layers are empty")
                console.log(obj.layers)
              }
            },
            error: function(error){
              console.log('error: ' + error)
            }
          });
    }, 500);
  }

   
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