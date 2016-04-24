from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,RequestContext
from .forms import RegisterForm, LoginForm
from .models import *
from django.http import HttpResponse

# Create your views here.
#

#def loginpage(request):
#    template = loader.get_template('login/Login.html')
#    context = RequestContext(request)
#    return HttpResponse(template.render(context,request))

def register(request):
    template = loader.get_template('login/Login.html')
    context = RequestContext(request)
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            Register = Registerer()

            if(not Register.SafeEmail(form.cleaned_data['Emailadres'])):
                context = {'message' : 'E-mail already used'}
                return HttpResponse(template.render(context,request))
            if(not Register.SafeUser(form.cleaned_data['Usernaam'])):
                context = {'message' : 'Username already used'}
                return HttpResponse(template.render(context,request))
            
            Register.Save(form.cleaned_data['Voornaam'],form.cleaned_data['Achternaam'],form.cleaned_data['Usernaam'],form.cleaned_data['Emailadres'],form.cleaned_data['Wachtwoord'])
            context = {'message':'SUCCES'}
            return HttpResponse(template.render(context,request))
        context = {'message':'Please fill in all fields'}
        return HttpResponse(template.render(context,request))
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))
	

def login(request):
    template = loader.get_template("login/Login.html")

    if (request.method == 'POST'):
        form=LoginForm(request.POST)
        if (form.is_valid()):
            context = {}
            Username = form.cleaned_data['Usernaam']
            Password = form.cleaned_data["Wachtwoord"]

            Validlogin = ValidLogin()
            if (Validlogin.isValid(Username, Password)):

                request.session['Username'] = Username
                request.session['UserID'] = Validlogin.getUserID()
                request.session['Language'] = "en" #By default
                if (Validlogin.hasHouse() == True):
                    request.session["HasHouse"] = True
                    request.session['HouseID'] = Validlogin.getFirstHouseID()
                else:
                    request.session['HasHouse'] = False
                request.session['IsAdmin'] = False

                request.session.modified = True

                context = {'message':'SUCCES'}
                response = HttpResponse(template.render(context))
                response.status_code = 202
                return response
            else:
                context = {'message':'Invalid password'}
                response = HttpResponse(template.render(context))
                response.status_code = 401
                return response

    elif (request.method == 'GET'):
        template = loader.get_template('login/Login.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

    context = RequestContext(request)
    response = HttpResponse(template.render(context))
    response.status_code = 404
    return response