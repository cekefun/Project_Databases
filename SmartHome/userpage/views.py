from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from django.http import Http404
from models import *

# Create your views here.


def indexpage(request):
	template = loader.get_template("userpage/index.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context, request))



def minuteusage(request):
	minutedata = MinuteData()
	resultobjects = minutedata.selectAll()

	template = loader.get_template("userpage/minuteusage.html")
	context = {
		'minutedata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def JSON_minuteusagehouse(request, householdid):
	minutedata = MinuteData()
	minutedata.selectByHouseholdID(householdid)
	return HttpResponse(minutedata.toJSON())


def JSON_hourusagehouse(request, householdid):
	hourdata = HourData()
	hourdata.selectByHouseholdID(householdid)
	return HttpResponse(hourdata.toJSON())


def JSON_dayusagehouse(request, householdid):
	daydata = DayData()
	daydata.selectByHouseholdID(householdid)
	return HttpResponse(daydata.toJSON())


def JSON_monthusagehouse(request, householdid):
	monthdata = MonthData()
	monthdata.selectByHouseholdID(householdid)
	return HttpResponse(monthdata.toJSON())


def JSON_yearusagehouse(request, householdid):
	yeardata = YearData()
	yeardata.selectByHouseholdID(householdid)
	return HttpResponse(yeardata.toJSON())


def hourlyusage(request):
	hourdata = HourData()
	resultobjects = hourdata.selectAll()

	template = loader.get_template("userpage/hourusage.html")
	context = {
		'hourdata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def dailyusage(request):

	daydata = DayData()
	resultobjects = daydata.selectAll()

	template = loader.get_template("userpage/dayusage.html")
	context = {
		'daydata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))



def monthlyusage(request):

	monthdata = MonthData()
	resultobjects = monthdata.selectAll()

	template = loader.get_template("userpage/monthusage.html")
	context = {
		'monthdata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def yearlyusage(request):

	yeardata = YearData()
	resultobjects = yeardata.selectAll()

	template = loader.get_template("userpage/yearusage.html")
	context = {
		'yeardata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def sensors(request):

	template = loader.get_template('userpage/sensor.html')
	context = {
		'hasHouse' : request.session["HasHouse"],
	}
	return HttpResponse(template.render(context, request))

#experimental code

def JSON_allsensors(request):

	resultobject = SensorData()
	resultobject.selectAll()

	return HttpResponse(resultobject.toJSON())


def JSON_allminutedata(request):

	resultobject = MinuteData()
	resultobject.selectAll()

	return HttpResponse(resultobject.toJSON())



def Update_sensordata(request):
	if (request.method == "POST"):
		# print request.POST.items()
		updateObj = SensorData()
		HasUpdated = updateObj.updateAttribute(request.POST['id'], request.POST['columnname'], request.POST['newvalue'])
		
		if (HasUpdated == True):
			return HttpResponse("everything okay.")
		else:
			response = HttpResponse("That title already exists for your household.")
			response.status_code = 400
			return response
	else:
		# print "Not accessing this view with POST request.... shit"
		return HttpResponse("<h1>Error 404: This page should be used with POST</h1>")

def Add_newSensor(request):
	if (request.method == "POST"):
		# print request.POST.items()
		# newSensor = Sensor()
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


def ChangeHouse(request):
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