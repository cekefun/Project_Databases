
function loadComments() {
	var SensorID = getCookie("SensorID");
	$.ajax({
		url:(String(SensorID) + "/"),
		type:'GET',
		success: function(text) {
			var dataobject = JSON.parse(text);
			displayAllComments(dataobject);
		}
	});
}

function displayAllComments(dataobject) {
	var amountComments = dataobject.comments.length;

	if (amountComments == 0) {
		$(".Comments").append("<p id='noCommentsMessage'>Er zijn nog geen opmerkingen voor deze sensor.</p>");
		$("#ListCurrentComments").hide();
		return;
	}

	for (var i = 0; i < amountComments; i++) {
		$("#ListCurrentComments").append("<li>" + dataobject.comments[i].Message + "</li>");
		if (i != amountComments-1) {
			$("#ListCurrentComments").append("<br>");
		}
	}

}

$("body").on("submit", "#FormNewComment", function(eventobject) {
	eventobject.preventDefault();
	var SensorID = getCookie("SensorID");
	var FormData = $("#FormNewComment").serialize();
	$.ajax({
		url:"addComment/",
		method:"POST",
		data:(FormData+"&"+$.param({"SensorID":SensorID})),
		success: function() {
			$("#noCommentsMessage").remove();
			$("#ListCurrentComments").show();
			$("#ListCurrentComments").append("<li>" + $("#NewMessage").val() + "</li>");
			$("#NewMessage").val("");
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


window.onload = loadComments