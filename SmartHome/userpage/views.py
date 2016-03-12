from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from models import *

# Create your views here.


def indexpage(request):

	template = loader.get_template("userpage/index.html")
	context = {}
	return HttpResponse(template.render(context, request))

	# return HttpResponse("Will contain a choice to view certain things, such as the daily data, overview, etc...")	

def minuteusage(request):
	minutedata = MinuteData()
	resultobjects = minutedata.selectAll()

	template = loader.get_template("userpage/minuteusage.html")
	context = {
		'minutedata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


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

