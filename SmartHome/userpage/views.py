from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from models import *

# Create your views here.


def indexpage(request):

	return HttpResponse("Will contain a choice to view certain things, such as the daily data, overview, etc...")	

def minuteusage(request):
	minutedata = MinuteData()
	resultobjects = minutedata.selectAll()

	template = loader.get_template("userpage/minuteusage.html")
	context = {
		'minutedata_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))



def dailyusage(request):

	return HttpResponse("Page to display the monthly data from a certain user.")


def sensors(request):

	sensordata = SensorData()
	resultobjects = sensordata.selectAll()

	template = loader.get_template('userpage/sensor.html')
	context = {
		'sensor_list' : resultobjects,
	}
	return HttpResponse(template.render(context, request))


def monthlyusage(request):


	return HttpResponse("Page to display the monthly data from a certain user.")