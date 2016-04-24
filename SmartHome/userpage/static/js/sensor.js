
function updateData(element) {
	var columnName = element.getAttribute("id");
	if (columnName == "Active") {
		updateActive(element);
	}
	var newValue = prompt("Enter new value.", ""); //TRANSLATE
	if (newValue == undefined)
		return;
	var sensorID = element.parentNode.getAttribute("sensorID");
	$.ajax({
		url:"updateSensor/",
		type:'POST',
		data: ($.param({"id":sensorID})+'&'+$.param({"columnname":columnName})+'&'+$.param({"newvalue":newValue})),
		success: function() {
			element.innerHTML = newValue;
		},
		error: function(context) {
			alert("The given value is not valid."); //TRANSLATE
			// alert(context.responseText);
		}
	});
}

function updateActive(element) {
	var columnName = "Active";
	var sensorID = element.parentNode.getAttribute("sensorID");
	var newValue = "0";
	if (element.getAttribute("value") == "0")
		newValue = "1";
	//update the active value in the database
	$.ajax({
		url:'updateSensor/',
		method:'POST',
		data: ($.param({"id":sensorID})+'&'+$.param({"columnname":columnName})+'&'+$.param({"newvalue":newValue})),
		success: function() {
			element.removeChild(element.firstChild);	
			if (newValue == "1") {
				element.appendChild(Checkmark());
				element.setAttribute("value", "1");
			}
			else {
				element.appendChild(Crossmark());
				element.setAttribute("value", "0");
			}
		},
		error: function() {
			alert("Could not change the active attribute of the sensor."); //TRANSLATE
		}
	});
}
function deleteSensor(element) {
	var result = window.confirm("Are you sure you want to delete the sensor? This will also delete all the data associated with it."); //TRANSLATE
	if (result == false) {
		return;
	}
	$.ajax({
		url: 'deleteSensor/',
		type: 'POST',
		data: $.param({'sensorID': element.parentNode.parentNode.getAttribute("sensorID")}),
		success: function() {
			LoadSensorData();
		}
	});
}

function showComments(element) {
	var SensorID = element.parentNode.parentNode.getAttribute("sensorID");
	document.cookie = "SensorID=" + SensorID + "; path=comments/";
	window.location = "comments/";
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
	}
});
$('body').on("submit", "#formNewSensor", function(eventobj) {
	eventobj.preventDefault();
	$.ajax({
		url: "addSensor/",
		type: "post",
		data: ($("#formNewSensor").serialize()),
		success: function() {
			finishForm();
		}
	});
});

function finishForm() {
	$("#btnAddNewSensor").show();
	cleanAddSensorForm();
	$(".formstyle").hide();
	LoadSensorData();
}

function cleanAddSensorForm() {
	$("input[name='Title']").val("");
	$("input[name='Apparature']").val("");
	$("input[name='Description']").val("");
	$("input[name='Unit']").val("");
}

function showSensorForm() {
	$(".formstyle").show();
	return;
}

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
function LoadSensorData() {
	var jsonhttp = new XMLHttpRequest();
	var url = "/index/sensors/current/";
	jsonhttp.onreadystatechange = function() {
		if (jsonhttp.readyState == 4 && jsonhttp.status == 200) {
			// console.log(jsonhttp.responseText);
			var sensordataobject = JSON.parse(jsonhttp.responseText);
			DisplaySensorDataTable(sensordataobject);
		}
		else if (jsonhttp.readyState == 4 && jsonhttp.status == 404) {
			console.log(jsonhttp.responseText);
		}
	}
	jsonhttp.open("GET", url, true);
	jsonhttp.send();
}
function DisplaySensorDataTable(dataobject) {
	var table = document.getElementById("sensortableinfo");
	var count = table.childNodes.length;
	for (var i = 2; i < count; i++) {
		table.removeChild(table.childNodes[2]);
	}
	
	for (i = 0; i < dataobject.sensors.length; i++) {
		//create table entries
		var tablerow = document.createElement("tr");
		tablerow.setAttribute("sensorID", dataobject.sensors[i].ID);
		
		//Apparature
		var tableelement_apparature = document.createElement("td");
		tableelement_apparature.setAttribute("ondblclick", "updateData(this)");
		tableelement_apparature.setAttribute("id","Apparature");
		var tableelement_apparature_text = document.createTextNode(dataobject.sensors[i].Apparature);
		//Title
		var tableelement_title = document.createElement("td");
		tableelement_title.setAttribute("ondblclick", "updateData(this)");
		tableelement_title.setAttribute("id", "Title");
		var tableelement_title_text = document.createTextNode(dataobject.sensors[i].Title);
		//Description
		var tableelement_description = document.createElement("td");
		tableelement_description.setAttribute("ondblclick", "updateData(this)");
		tableelement_description.setAttribute("id", "Description");
		var tableelement_description_text = document.createTextNode(dataobject.sensors[i].Description);
		//Unit
		var tableelement_unit = document.createElement("td");
		tableelement_unit.setAttribute("ondblclick", "updateData(this)");
		tableelement_unit.setAttribute("id", "Unit");
		var tableelement_unit_text = document.createTextNode(dataobject.sensors[i].Unit);
		//Active
		var tableelement_active = document.createElement("td");
		tableelement_active.setAttribute("id", "Active");
		tableelement_active.setAttribute("ondblclick", "updateActive(this)");
		//DELETE
		var tableelement_delete = document.createElement("td");
		var delete_icon = TrashBin()
		delete_icon.setAttribute("onclick", "deleteSensor(this)");
		//SHOWCOMMENTS
		var tableelement_comments = document.createElement("td");
		var tableelement_commentsbutton = document.createElement("button");
		tableelement_commentsbutton.setAttribute("class", "commentButton");
		tableelement_commentsbutton.setAttribute("onclick", "showComments(this)");
		tableelement_commentsbutton.appendChild(document.createTextNode("Show comments"));

		tableelement_comments.appendChild(tableelement_commentsbutton);
		tableelement_delete.appendChild(delete_icon);
		tableelement_apparature.appendChild(tableelement_apparature_text);
		tableelement_title.appendChild(tableelement_title_text);
		tableelement_description.appendChild(tableelement_description_text);
		tableelement_unit.appendChild(tableelement_unit_text);
		if (dataobject.sensors[i].Active == 1) {
			tableelement_active.appendChild(Checkmark());
			tableelement_active.setAttribute("value", "1");
		}
		else {
			tableelement_active.appendChild(Crossmark());
			tableelement_active.setAttribute("value", "0");
		}
		tablerow.appendChild(tableelement_title);
		tablerow.appendChild(tableelement_apparature);
		tablerow.appendChild(tableelement_description);
		tablerow.appendChild(tableelement_unit);
		tablerow.appendChild(tableelement_active);
		tablerow.appendChild(tableelement_delete);
		tablerow.appendChild(tableelement_comments);
		table.appendChild(tablerow);
	}
}
function Checkmark() {
	var checkmark = document.createElement("span");
	checkmark.setAttribute("class", "checkmark");
	var div1 = document.createElement("div");
	div1.setAttribute("class", "checkmark_circle");
	var div2 = document.createElement("div");
	div2.setAttribute("class", "checkmark_stem");
	var div3 = document.createElement("div");
	div3.setAttribute("class", "checkmark_kick");
	checkmark.appendChild(div1);
	checkmark.appendChild(div2);
	checkmark.appendChild(div3);
	return checkmark;
}
function Crossmark() {
	var crossmark = document.createElement("span");
	crossmark.setAttribute("class", "crossmark");
	var div1 = document.createElement("div");
	div1.setAttribute("class", "crossmark_circle");
	var div2 = document.createElement("div");
	div2.setAttribute("class", "crossmark_slash");
	var div3 = document.createElement("div");
	div3.setAttribute("class", "crossmark_backslash");
	crossmark.appendChild(div1);
	crossmark.appendChild(div2);
	crossmark.appendChild(div3);
	return crossmark;
}
function TrashBin() {
	var trashbin = document.createElement("div");
	trashbin.setAttribute("class", "icon-trash");
	trashbin.setAttribute("style", "float: left");
	var trashlid = document.createElement("div");
	trashlid.setAttribute("class", "trash-lid");
	trashlid.setAttribute("style", "background-color: #03A7D7");
	trashbin.appendChild(trashlid);
	var trashcontainer = document.createElement("div");
	trashcontainer.setAttribute("class", "trash-container");
	trashcontainer.setAttribute("style", "background-color: #02A7D7");
	trashbin.appendChild(trashcontainer);
	var trashline1 = document.createElement("div");
	trashline1.setAttribute("class", "trash-line-1");
	trashbin.appendChild(trashline1);
	var trashline2 = document.createElement("div");
	trashline2.setAttribute("class", "trash-line-2");
	trashbin.appendChild(trashline2);
	var trashline3 = document.createElement("div");
	trashline3.setAttribute("class", "trash-line-3");
	trashbin.appendChild(trashline3);
	return trashbin;
}
window.onload = LoadSensorData;