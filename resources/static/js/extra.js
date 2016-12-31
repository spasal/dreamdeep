$(function() {

    // save file
    $(".member").click(function(){
        var filename = $(this).val()
        var recipient = prompt("Please enter your e-mail")
        if(isValidEmailAddress(recipient)){
            data = {
                filename: filename,
                recipient: recipient
            }

            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: '/api/save_dream',
                data: JSON.stringify(data),
                success: function(response) {
                    console.log('success: ' + response)
                },
                error: function(error) {
                    console.log('error: ' + error)
                }
            });
        }else{
            alert("You didn't enter a valid e-mail address")
        }
    });

    function isValidEmailAddress(emailAddress) {
        var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
        return pattern.test(emailAddress);
    };

});
