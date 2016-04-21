from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader,RequestContext
from django.http import HttpResponse

# Create your views here.
#

def loginpage(request):
    template = loader.get_template('admin/AdminLogin.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context,request))


