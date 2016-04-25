from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader, RequestContext
from models import *

# Create your views here.


def homepageForum(request):

	return HttpResponse("Forum homepage.")


def showWall(request, wallname):
	return HttpResponse(str(wallname))
