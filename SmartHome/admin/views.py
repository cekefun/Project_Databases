from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,RequestContext
from .forms import *
from django.http import HttpResponse,HttpResponseNotFound
from .models import *
import datetime


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
                request.session['Language'] = "en" #By default
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
    if(not request.session['IsAdmin']):
        return HttpResponseNotFound('<h1>Page not found</h1>')
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

def reportpage(request):
    if(not request.session['IsAdmin']):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    template = loader.get_template("admin/reportForm.html")
    context = {}
    return HttpResponse(template.render(context, request))

def getreport(request):
    if(request.method == 'POST'):
        form = RequestForm(request.POST)
        if(form.is_valid()):
            aggr = AdminAgg()
            startDate=form.cleaned_data['start']
            endDate = form.cleaned_data['to']
            if(endDate < startDate):
                return HttpResponseNotFound('<h1>Page not found</h1>')

            startDate = datetime.datetime.combine(startDate, datetime.time.min)
            endDate = datetime.datetime.combine(endDate, datetime.time.min)
            endDate += datetime.timedelta(days=1)
            endDate -= datetime.timedelta(minutes=1)

            startDate = startDate.isoformat(sep=' ')
            endDate = endDate.isoformat(sep=' ')

            kind = form.cleaned_data['selecttime']
            table = ""
            if (kind == 'minute'):
                table = "MinuteData"
            elif (kind == 'hour'):
                table = "HourData"
            elif (kind == 'day'):
                table = "DayData"
            elif (kind == 'month'):
                table = 'MonthData'
            elif (kind == 'year'):
                table = 'YearData'
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
            
            kind = form.cleaned_data['selectregion']
            region = ""
            regionKind = ""
            if (kind == 'streetnamecity'):
                regionKind = "City"
                if(form.cleaned_data['city'] == ""):
                    return HttpResponseNotFound('<h1>Page not found</h1>')
                if(form.cleaned_data['streetname'] != ""):
                    aggr.searchStreet(table,startDate,endDate,form.cleaned_data['streetname'],form.cleaned_data['city'])
                else:
                    aggr.search(table,startDate,endDate,'City',form.cleaned_data['city'])
            elif (kind == 'postalcode'):
                if(form.cleaned_data['postalcode'] == ""):
                    return HttpResponseNotFound('<h1>Page not found</h1>')
                aggr.search(table,startDate,endDate,'PostalCode',form.cleaned_data['postalcode'])
            elif (kind == 'country'):
                if(form.cleaned_data['country'] == ""):
                    return HttpResponseNotFound('<h1>Page not found</h1>')
                aggr.search(table,startDate,endDate,'Country',form.cleaned_data['country'])
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
            return HttpResponse(aggr.toJson())
        return HttpResponse('FORM IS NOT VALID')
    return HttpResponse('Thats not a post')
