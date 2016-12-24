$(function () {

   $("#start_dream").click(function() {
    console.log($("#iteration").value)
   	data = {
   		iteration: "val1",
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