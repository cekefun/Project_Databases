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
                    request.session["HasHouse"] = True
                    request.session['HouseID'] = Validlogin.getFirstHouseID()
                else:
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
    if(request.session['Language'] == 'nl'):
        template = loader.get_template("admin/UserPage_nl.html")
    else:
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
            if(request.session['Language'] == 'nl'):
                return HttpResponse(request.POST['UserName']+"is nu een admin.")
            else:
                return HttpResponse(request.POST['UserName']+"is now an admin.")
        return HttpResponse("<h1>Error 404: Page not found</h1>")
    return HttpResponse("<h1>Error 404: Page not found</h1>")

def getreport(request):
    if(not request.session['IsAdmin']):
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if(request.session['Language'] == 'nl'):
        template = loader.get_template("admin/reportForm_nl.html")
    else:
        template = loader.get_template("admin/reportForm.html")
    if(request.method == 'POST'):
        form = RequestForm(request.POST)
        if(form.is_valid()):
            aggr = AdminAgg()
            startDate=form.cleaned_data['start']
            endDate = form.cleaned_data['to']
            if(endDate < startDate):
                if(request.session['Language'] == 'nl'):
                    context = {'message':'Startdatum is na de einddatum'}
                else:
                    context = {'message':'Startdate falls after the enddate'}
                return HttpResponse(template.render(context, request))

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
                if(request.session['Language'] == 'nl'):
                    context = {'message': 'Kies alstublieft een type data'}
                else:
                    context = {'message': 'Please choose a sampletype'}
                return HttpResponse(template.render(context, request))
            
            kind = form.cleaned_data['selectregion']
            region = ""
            regionKind = ""
            if (kind == 'streetnamecity'):
                regionKind = "City"
                if(form.cleaned_data['city'] == ""):
                    if(request.session['Language'] == 'nl'):
                        context = {'message': 'Geef alstublieft een stad'}
                    else:
                        context = {'message': 'Please write down a city'}
                    return HttpResponse(template.render(context, request))
                if(form.cleaned_data['streetname'] != ""):
                    aggr.searchStreet(table,startDate,endDate,form.cleaned_data['streetname'],form.cleaned_data['city'])
                else:
                    aggr.search(table,startDate,endDate,'City',form.cleaned_data['city'])
            elif (kind == 'postalcode'):
                if(form.cleaned_data['postalcode'] == ""):
                    if(request.session['Language'] == 'nl'):
                        context = {'message': 'Geef alstublieft een postcode'}
                    else:
                        context = {'message': 'Please write down a postalcode'}
                    return HttpResponse(template.render(context, request))
                aggr.search(table,startDate,endDate,'PostalCode',form.cleaned_data['postalcode'])
            elif (kind == 'country'):
                if(form.cleaned_data['country'] == ""):
                    if(request.session['Language'] == 'nl'):
                        context = {'message': 'Geef alstublieft een land'}
                    else:
                        context = {'message': 'Please write down a country'}
                    return HttpResponse(template.render(context, request))
                aggr.search(table,startDate,endDate,'Country',form.cleaned_data['country'])
            else:
                if(request.session['Language'] == 'nl'):
                    context = {'message': 'Selecteer alstublieft een regio'}
                else:
                    context = {'message': 'Please select a region'}
                return HttpResponse(template.render(context, request))
            return HttpResponse(aggr.toJson())
        if(request.session['Language'] == 'nl'):
            context = {'message': 'Vul alstublieft alle velden in'}            
        else:
            context = {'message': 'Please fill in all fields'}
        return HttpResponse(template.render(context, request))
    context = {'message': ''}
    return HttpResponse(template.render(context, request))

