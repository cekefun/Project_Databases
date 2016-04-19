from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,RequestContext
from .forms import RegisterForm
from .models import *
from django.http import HttpResponse

# Create your views here.


def loginpage(request):
    template = loader.get_template('login/Login.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            Register = Registerer()
            Register.Save(form.cleaned_data['Voornaam'],form.cleaned_data['Achternaam'],form.cleaned_data['Usernaam'],form.cleaned_data['Emailadres'],form.cleaned_data['Wachtwoord'])
            return HttpResponse("Zou gelukt moeten zijn")
    return HttpResponse("Er is iets misgegaan")
	
