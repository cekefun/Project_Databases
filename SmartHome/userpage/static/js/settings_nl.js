

function insertAllHousesTable(dataobject) {
	for (var i = 0; i < dataobject.houses.length; i++) {
		$("#householdtable").append("<tr HouseID='" + dataobject.houses[i].ID + "'><td>" + dataobject.houses[i].Streetname + "</td><td>" + dataobject.houses[i].Streetnumber + "</td><td>"+ dataobject.houses[i].City + "</td><td>" + dataobject.houses[i].Postalcode + "</td><td>" + dataobject.houses[i].Country + "</td><td ondblclick='updatePrice(this);'>" + dataobject.houses[i].Price + "</td></tr>");
	}
}

function setupChangeHouseholds(dataobject) {
	var shouldAddForm = dataobject.houses.length > 1 ? true : false;

	//if the user has more than 1 house --> add entries to the form
	if (shouldAddForm == true) {
		$("<p id='otherHouseHoldsText'>Andere huishoudens:</p>").insertBefore("#changehouseholdform");
		$("#changehouseholdform").append("<select name='NewHouse' id='selecthouseholds'></select>");
	}

	for (var i = 0; i < dataobject.houses.length; i++) {
		//add the data to the current list if it is the one used in the current session
		if (dataobject.houses[i].CurrentlyActive == 1) {
			$("#currenthousehold").append("<tr HouseID='" + dataobject.houses[i].ID + "'><td>" + dataobject.houses[i].Streetname + "</td><td>" + dataobject.houses[i].Streetnumber + "</td><td>"+ dataobject.houses[i].City + "</td><td>" + dataobject.houses[i].Country + "</td></tr>");
		}
		//add all the other households to the select form
		else {
			var strHouse = String(dataobject.houses[i].Streetname) + "-" + String(dataobject.houses[i].Streetnumber) + "-" + String(dataobject.houses[i].City) + "-" + String(dataobject.houses[i].Country); 
			var HouseID = String(dataobject.houses[i].ID);
			$("#selecthouseholds").append("<option value='" + HouseID + "'>" + strHouse + "</option>");
		}
	}

	//if the user has more than one house, add a submit button to the form
	if (shouldAddForm == true) {
		$("#changehouseholdform").append("&nbsp;&nbsp;&nbsp;<input type='submit' value='Verander van huishouden'>");
	}
}

function insertCurrentHouse(dataobject) {	
	for (var i = 0; i < dataobject.houses.length; i++) {
		if (dataobject.houses[i].CurrentlyActive == 1) {
			$("#currenthousehold").append("<tr HouseID='" + dataobject.houses[i].ID + "'><td>" + dataobject.houses[i].Streetname + "</td><td>" + dataobject.houses[i].Streetnumber + "</td><td>"+ dataobject.houses[i].City + "</td><td>" + dataobject.houses[i].Country + "</td></tr>");
		}
	}
}

function loadHouseholds() {
	$.ajax({
		url:"currentHouseholds/",
		type:"get",
		success: function(text) {
			var dataobject = JSON.parse(text);
			insertAllHousesTable(dataobject);
			setupChangeHouseholds(dataobject);
		},
		error: function() {
			console.log("failed to load the data.");
		}
	});
}

function updatePrice(element) {
	var newPrice = prompt("Geef een nieuwe prijs in."); //TRANSLATE
	if (newPrice == "" || newPrice == null)
		return;

	newPrice = parseFloat(newPrice);

	if (newPrice === NaN) {
		alert("De waarde die u ingegeven heeft is niet geldig.");
		return;
	}

	var houseid = element.parentNode.getAttribute("HouseID");

	$.ajax({
		url:"updatePrice/",
		type:"POST",
		data:($.param({"HouseID":houseid})+"&"+$.param({"Price":newPrice})),
		success: function() {
			element.innerHTML = String(newPrice);
		},
		error: function() {
			alert("Het lukte niet om de prijs/eenheid van uw huis aan te passen."); //TRANSLATE
		}
	});
}

function clearChangeHouseholds() {
	$("#changehouseholdform").html("");
	$("#currenthousehold").html("");
	$("#otherHouseHoldsText").remove();
}

function reloadChangeHouseholds() {
	//reload the current household data and load it in the table/form
	$.ajax({
		url:'currentHouseholds/',
		type:"GET",
		success: function(text) {
			var dataobject = JSON.parse(text);
			setupChangeHouseholds(dataobject);
		}
	});
}

$("body").on("submit", "#changehouseholdform", function(eventobject) {
	eventobject.preventDefault();
	$.ajax({
		url:"changeHouse/",
		type:"POST",
		data:($("#changehouseholdform").serialize()),
		success: function() {
			clearChangeHouseholds();
			reloadChangeHouseholds();
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

window.onload = loadHouseholds