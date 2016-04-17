from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.indexpage, name='indexpage'),
	url(r'^sensors/$', views.sensors, name='sensors'),
	url(r'^minute/$', views.minuteusage, name ='minuteuse'),
	url(r'^minute/(?P<householdid>[0-9]*)/$', views.JSON_minuteusagehouse, name='minuteusehousehold'),
    url(r'^hour/$', views.hourlyusage, name='hourlyuse'),
    url(r'^hour/(?P<householdid>[0-9]*)/$', views.JSON_hourusagehouse, name='hourusehouse'),
    url(r'^day/$', views.dailyusage, name='dailyuse'),
    url(r'^day/(?P<householdid>[0-9]*)/$', views.JSON_dayusagehouse, name='dayusehouse'),
    url(r'^month/$', views.monthlyusage, name='monthlyuse'),
    url(r'^month/(?P<householdid>[0-9]*)/$', views.JSON_monthusagehouse, name='monthusehouse'),
    url(r'^year/$', views.yearlyusage, name='yearlyuse'),
    url(r'^year/(?P<householdid>[0-9]*)/$', views.JSON_yearusagehouse, name='yearusehouse'),
    # url(r'^sensors/(?P<householdid>[0-9]*/$)', views.JSON_sensorhouse, name='sensorhouse'),
    url(r'^sensors/updateSensor/$', views.Update_sensordata, name='updateSensordata'),
    url(r'^sensors/addSensor/$', views.Add_newSensor, name="addNewSensor"),

    url(r'^sensors/all$', views.JSON_allsensors, name="jsonsensordata"), #used for testing
    url(r'^minute/all$', views.JSON_allminutedata, name='jsonminutedata'), #used for testing
]