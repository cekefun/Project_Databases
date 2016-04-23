


$('body').on("submit", "#newHouse", function(eventobj) {
	eventobj.preventDefault();
	$.ajax({
		url: "",
		type: "post",
		data: ($("#newHouse").serialize()),
		success: function() {
			$(".errorMessage").hide();
			$(".successMessage").show();
			cleanform();
		},
		error: function() {
			$(".errorMessage").show();
			$(".successMessage").hide();
			cleanform();
		}
	});
});

function cleanform() {
	$("input[name='Streetname']").val("");
	$("input[name='Streetnumber']").val("");
	$("input[name='City']").val("");
	$("input[name='Postalcode']").val("");
	$("input[name='Country']").val("");
	$("input[name='Price']").val("");
}


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