from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.indexpage, name='indexpage'),
	url(r'^sensors/$', views.sensors, name='sensors'),
	url(r'^minute/$', views.minuteusage, name ='minuteuse'),
    url(r'^hour/$', views.hourlyusage, name='hourlyuse'),
    url(r'^day/$', views.dailyusage, name='dailyuse'),
    url(r'^month/$', views.monthlyusage, name='monthlyuse'),
    url(r'^year/$', views.yearlyusage, name='yearlyuse'),
    url(r'^sensors/all$', views.jsonallsensors, name="jsonsensordata"),
    url(r'^minute/all$', views.jsonallminutedata, name='jsonminutedata'),
]