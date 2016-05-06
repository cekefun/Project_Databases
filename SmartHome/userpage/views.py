from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from django.http import Http404
from models import *
from .forms import HouseForm


def IsLoggedIn(request):
	""" Checks if the session is configured """

	if ("UserID" not in request.session):
		return False
	return True

def RedirectNotLoggedIn(request):
	return redirect('/login/')





def indexPage(request):
#	if (IsLoggedIn(request) == False):
#		return RedirectNotLoggedIn(request)


	if ("Language" not in request.session): #when the user hasn't visited the site yet
		 request.session["Language"] = "en"

	language = request.session["Language"]

	htmlpage = "userpage/Home.html"
	language = "en"
	if("Language" in request.session):
		language = request.session["Language"]


	if (language == "nl"):
		htmlpage = "userpage/Home_nl.html" #MIGHT STILL NEED TO CHANGE
	else:
		htmlpage = "userpage/Home.html"
	template = loader.get_template(htmlpage)
	context = RequestContext(request)
	return HttpResponse(template.render(context, request))



def minuteusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/minuteusage.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/minuteusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/minuteusage_nl.html" #MIGHT STILL NEED TO CHANGE

	minutedata = MinuteData()
	resultobjects = minutedata.selectAll()

	template = loader.get_template(htmlpage)
	context = {
		'minutedata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def hourlyusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/hourusage.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/hourusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/hourusage_nl.html" #MIGHT STILL NEED TO CHANGE


	hourdata = HourData()
	resultobjects = hourdata.selectAll()

	template = loader.get_template(htmlpage)
	context = {
		'hourdata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def dailyusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/dayusage.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/dayusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/dayusage_nl.html" #MIGHT STILL NEED TO CHANGE

	daydata = DayData()
	resultobjects = daydata.selectAll()

	template = loader.get_template(htmlpage)
	context = {
		'daydata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))

def weeklyusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/weekusage.html"
	language = request.session["Language"]

	if (language =="en"):
		htmlpage = "userpage/weekusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/weekusage_nl.html"

	template = loader.get_template(htmlpage)
	context = {	}
	return HttpResponse(template.render(context, request))


def monthlyusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/monthusage.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/monthusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/monthusage_nl.html" #MIGHT STILL NEED TO CHANGE

	monthdata = MonthData()
	resultobjects = monthdata.selectAll()

	template = loader.get_template(htmlpage)
	context = {
		'monthdata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def yearlyusage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/yearusage.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/yearusage.html"
	elif (language == "nl"):
		htmlpage = "userpage/yearusage_nl.html" #MIGHT STILL NEED TO CHANGE

	yeardata = YearData()
	resultobjects = yeardata.selectAll()

	template = loader.get_template(htmlpage)
	context = {
		'yeardata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def sensors(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/sensor.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/sensor.html"
	elif (language == "nl"):
		htmlpage = "userpage/sensor_nl.html"

	template = loader.get_template(htmlpage)
	context = {
		'hasHouse' : request.session["HasHouse"],
	}
	return HttpResponse(template.render(context, request))


def ChangeHouse(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)
	
	if (request.method == 'POST'):
		#Might need to be changed slightly later on

		newHouseID = request.POST["HouseID"]
		request.session["HouseID"] = newHouseID

		response = HttpResponse("Successfully changed house.")
		response.status_code = 200
		return response

	else:
		response = HttpResponse("This page can only be used for POST requests.")
		response.status_code = 404
		return response


def Update_sensordata(request):
	if (request.method == "POST"):
		updateObj = SensorData()
		HasUpdated = updateObj.updateAttribute(request.POST['id'], request.POST['columnname'], request.POST['newvalue'])
		
		if (HasUpdated == True):
			return HttpResponse("everything okay.")
		else:
			response = HttpResponse("That title already exists for your household.")
			response.status_code = 400
			return response
	else:
		return HttpResponse("<h1>Error 404: This page should be used with POST</h1>")

def Add_newSensor(request):
	if (request.method == "POST"):
		if (request.session["HasHouse"] == False):
			response = HttpResponse("No house to add a sensor to")
			response.status_code = 404
			return response

		AddNewSensor(request.session["HouseID"], request.POST["Title"], request.POST["Apparature"], request.POST["Description"], request.POST["Unit"])
		result = HttpResponse("Sensor added.")
		result.status_code = 200
		return result
	else:
		result = HttpResponse("<h1>Error 404: This page should be used with POST</h1>")
		result.status_code = 404
		return result

def Delete_sensor(request):
	if (request.method == "POST"):

		DeleteSensor(request.POST["sensorID"])

		result = HttpResponse("Sensor deleted.")
		result.status_code = 200
		return result

	else:
		result = HttpResponse("<h1>Error 404: This page should be used with POST</h1>")
		result.status_code = 404
		return result

def CurrentTitleSensors(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	return HttpResponse(SensorTitle(request.session["HouseID"]).getCurrentSensorTitlesJSON())


def addHouse(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	if (request.method == "POST"):
		form = HouseForm(request.POST)
		if (form.is_valid()):
			newhouse = NewHouse(form, request.session["UserID"])
			isFirst = newhouse.isFirst()
			newhouse.addToDatabase()
			if (isFirst == True):
				request.session["HasHouse"] = True
				request.session["HouseID"] = getFirstHouseID(request.session["UserID"])
			return HttpResponse("New house succesfully added.")

		else:
			response = HttpResponse("Not all fields are filled in.")
			response.status_code = 400
			return response

	elif (request.method == "GET"):

		htmlpage = "userpage/addHouse.html"
		language = request.session["Language"]

		if (language == "en"):
			htmlpage = "userpage/addHouse.html"
		elif (language == "nl"):
			htmlpage = "userpage/addHouse_nl.html"

		template = loader.get_template(htmlpage)
		context = {}
		return HttpResponse(template.render(context, request))


	else:
		result = HttpResponse("This page should be used with a get/post request.")
		result.status_code = 404
		return result


def aboutPage(request):
	# if (IsLoggedIn(request) == False):
	# 	return RedirectNotLoggedIn(request)


	if ("Language" not in request.session): #when the user hasn't visited the site yet
		 request.session["Language"] = "en"

	htmlpage = "userpage/About.html"
	language = request.session["Language"]

	if (language == "nl"):
		htmlpage = "userpage/About_nl.html"

	template = loader.get_template(htmlpage)
	context = {}
	return HttpResponse(template.render(context, request))


def settingsPage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlpage = "userpage/settings.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlpage = "userpage/settings.html"
	elif (language == "nl"):
		htmlpage = "userpage/settings_nl.html"

	template = loader.get_template(htmlpage)
	context = {}
	return HttpResponse(template.render(context, request))


def updatePrice(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	if (request.method == 'POST'):
		HouseID = int(request.POST["HouseID"])
		Price = float(request.POST["Price"])

		updatePriceByHouseholdID(HouseID, Price)
		return HttpResponse("Price changed.")



	response = HttpResponse("This page should be used with a post request.")
	response.status_code = 400
	return response


def changeLanguage(request):
	if (request.method == "POST"):
		newLang = request.POST["language"]

		request.session["Language"] = newLang
		return HttpResponse("Language changed.")

	response = HttpResponse("This page should be used with a post request.")
	response.status_code = 400
	return response


def changeCurrentHouse(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	if (request.method == "POST"):
		NewHouseID = int(request.POST["NewHouse"])
		request.session["HouseID"] = NewHouseID
		return HttpResponse("Succesfully changed household.")

	response = HttpResponse("This page should be used with a post request.")
	response.status_code = 400
	return response



def commentsPage(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	htmlfile = "userpage/comments.html"
	language = request.session["Language"]

	if (language == "en"):
		htmlfile = "userpage/comments.html"
	elif (language == "nl"):
		htmlfile = "userpage/comments_nl.html"

	template = loader.get_template(htmlfile)
	context = {}
	return HttpResponse(template.render(context, request))


def addCommentSensor(request):
	if (request.method == 'POST'):
		SensorID = request.POST["SensorID"]
		CommentText = request.POST["Message"]
		addComment(SensorID, CommentText)
		return HttpResponse("Added comment to your sensor.")



	response = HttpResponse("This page should be used with a post request.")
	response.status_code = 400
	return response









def JSON_minuteusagehouse(request, householdid):
	minutedata = MinuteData()
	minutedata.selectByHouseholdID(householdid)
	return HttpResponse(minutedata.toJSON(householdid))


def JSON_hourusagehouse(request, householdid):
	hourdata = HourData()
	hourdata.selectByHouseholdID(householdid)
	return HttpResponse(hourdata.toJSON(householdid))


def JSON_dayusagehouse(request, householdid):
	daydata = DayData()
	daydata.selectByHouseholdID(householdid)
	return HttpResponse(daydata.toJSON(householdid))


def JSON_monthusagehouse(request, householdid):
	monthdata = MonthData()
	monthdata.selectByHouseholdID(householdid)
	return HttpResponse(monthdata.toJSON(householdid))


def JSON_yearusagehouse(request, householdid):
	yeardata = YearData()
	yeardata.selectByHouseholdID(householdid)
	return HttpResponse(yeardata.toJSON(householdid))


def JSON_allsensors(request):

	resultobject = SensorData()
	resultobject.selectAll()

	return HttpResponse(resultobject.toJSON())


def JSON_allminutedata(request):

	resultobject = MinuteData()
	resultobject.selectAll()

	return HttpResponse(resultobject.toJSON())




def JSON_CurrentSensors(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	sensorData = SensorData()
	sensorData.selectByHouseHoldID(request.session["HouseID"])


	return HttpResponse(sensorData.toJSON())

def JSON_CurrentMinuteData(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	return JSON_minuteusagehouse(request, request.session["HouseID"])

def JSON_CurrentHourData(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	return JSON_hourusagehouse(request, request.session["HouseID"])

def JSON_CurrentDayData(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	return JSON_dayusagehouse(request, request.session["HouseID"])


def JSON_CurrentMonthData(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	return JSON_monthusagehouse(request, request.session["HouseID"])


def JSON_CurrentYearData(request):
	if (request.session["HasHouse"] == False):
		result = HttpResponse("You don't own a house.")
		result.status_code = 404
		return result

	return JSON_yearusagehouse(request, request.session["HouseID"])


def JSON_householdsprice(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	if (request.session["HasHouse"] == False):
		return HttpResponse('{"houses":[]}')

	return HttpResponse(HouseHoldsPrice(request.session["UserID"], request.session["HouseID"]).getHousesJSON())

def JSON_commentssensor(request, sensorID):
	return HttpResponse(CommentsFromSensor(sensorID).getCommentsJSON())


def JSON_CurrentMinute(request):
	if (IsLoggedIn(request) == False):
		return RedirectNotLoggedIn(request)

	household = request.session["HouseID"]

	return HttpResponse(currentMinuteUsage(household).getSamples())
