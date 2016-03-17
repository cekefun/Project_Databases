import os

from django.shortcuts import render_to_response
from .models import CSVDecoder , save_uploaded_file
from .forms import UploadFileForm
from django.template import RequestContext,loader
from django.http import HttpResponse


# Create your views here.

def uploadPage(request):
    #template = loader.get_template("SensorClient/uploadTemp.html")
    
    return render_to_response('SensorClient/uploadTemp.html', context_instance=RequestContext(request))

    

def upload(request):
    template = loader.get_template("SensorClient/uploadTemp.html")
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            name = save_uploaded_file(request.FILES['file'])
            decoder = CSVDecoder()
            decoder.Decode(name, 1)        #Die 1 moet ik nog aanpassen
            os.remove(name)
            return HttpResponse("Zou gedaan moeten zijn")
    if request.method == 'PUT':
        form = UploadFileForm(request.PUT,request.data)
        if form.is_valid():
            name = save_uploaded_file(request.data)
            decoder = CSVDecoder()
            decoder.Decode(name, 1)        #Die 1 moet ik nog aanpassen
            os.remove(name)
            return HttpResponse("Zou gedaan moeten zijn")

    return HttpResponse("Zou mislukt moeten zijn")

