$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});



$("body").on("submit", ".login-form", function(eventobj) {
	eventobj.preventDefault();

	$.ajax({
		url: "",
		type: "post",
		data: ($(".login-form").serialize()),

		success: function() {
			// alert("Succesfull login.");
			// console.log("Succesfull login.");
			window.location.replace("../");
		},
		error: function() {
			alert("Login failed.");
			// console.log("Login failed.")
			document.getElementById("WachtwoordLogin").value = "";
		}
	});

});


$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
	}
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}







/*
		headers: {
			"X-CSRFToken": getCookie("csrftoken")
		},
*/

// $("body").bind("ajaxSend", function(elm, xhr, s){
//    if (s.type == "POST") {
//       xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
//    }
// });