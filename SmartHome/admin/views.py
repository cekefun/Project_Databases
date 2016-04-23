from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,RequestContext
from .forms import *
from django.http import HttpResponse
from .models import *

# Create your views here.
#

def loginpage(request):
    template = loader.get_template('admin/AdminLogin.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))

def login(request):
    template = loader.get_template("admin/AdminLogin.html")

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
                if (Validlogin.hasHouse() == True):
                    print "He has a house."
                    request.session["HasHouse"] = True
                    request.session['HouseID'] = Validlogin.getFirstHouseID()
                else:
                    print "He doesn't have a house."
                    request.session['HasHouse'] = False
                request.session['IsAdmin'] = True

                context = {'message':'SUCCES'}
                response = HttpResponse(template.render(context))
                response.status_code = 202
                return response
            else:
                context = {'message':'Invalid password'}
                response = HttpResponse(template.render(context))
                response.status_code = 401
                return response


    context = RequestContext(request)
    response = HttpResponse(template.render(context))
    response.status_code = 404
    return response

def users(request):
    template = loader.get_template("admin/UserPage.html")
    searcher=AdminSearch()
    searcher.users()
    results = searcher.getResults()
    context = {'user_list' : results}
    return HttpResponse(template.render(context, request))

def UpdateAdmin(request):
    if(request.method == 'POST'):
        form=UserForm(request.POST)
        if(form.is_valid()):
            updater = AdminSearch()
            updater.makeAdmin(request.POST['UserName'])
            return HttpResponse("everything okay.")
        return HttpResponse("<h1>Error 404: Something went wrong in making the form</h1>")
    return HttpResponse("<h1>Error 404: This page should be used with POST</h1>")
    
