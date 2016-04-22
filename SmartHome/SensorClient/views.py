import os

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import UploadFileForm , UploadjsonForm
from django.template import RequestContext,loader
from django.http import HttpResponse


# Create your views here.
@csrf_exempt
def uploadCSVPage(request):
    template = loader.get_template("SensorClient/uploadTemp.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))

    
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            name = save_uploaded_csvfile(form.cleaned_data['Uplfile'])
            decoder = CSVDecoder()
            decoder.Decode(name, form.cleaned_data['household'])
            os.remove(name)
            return uploadCSVPage(request)
    return uploadCSVPage(request)

@csrf_exempt
def uploadPage(request):
    template = loader.get_template("SensorClient/uploadFam.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))


@csrf_exempt
def upload_json(request):
    if request.method == 'POST':
        form = UploadjsonForm(request.POST,request.FILES)
        if form.is_valid():
            name = save_uploaded_jsonfile(form.cleaned_data['Uplfile'])
            decoder = jsonDecoder()
            decoder.Decode(name)
            os.remove(name)
            return uploadPage(request)
    return uploadPage(request)

