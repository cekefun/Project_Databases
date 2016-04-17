from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from models import *

# Create your views here.


def indexpage(request):

	request.session['UserID'] = 'testing'
	del request.session['UserID']
	template = loader.get_template("userpage/index.html")
	context = {}
	return HttpResponse(template.render(context, request))



def minuteusage(request):
	if ('UserID' in request.session):
		print "key = ", request.session['UserID']
	else:
		print "the key doesn't exist for this session yet."

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

	sensordata = SensorData()
	resultobjects = sensordata.selectAll()

	template = loader.get_template('userpage/sensor.html')
	context = {
		'sensor_list' : resultobjects,
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
		print request.POST.items()
		updateObj = SensorData()
		updateObj.updateAttribute(request.POST['id'], request.POST['columnname'], request.POST['newvalue'])
		return HttpResponse("everything okay.")



	else:
		print "Not accessing this view with POST request.... shit"