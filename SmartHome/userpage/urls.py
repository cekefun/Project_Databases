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

    url(r'^sensors/updateSensor/$', views.Update_sensordata, name='updateSensordata'),
    url(r'^sensors/addSensor/$', views.Add_newSensor, name="addNewSensor"),
    url(r'^sensors/deleteSensor$', views.Delete_sensor, name="deleteSenor"),
    
    url(r'^sensors/current/$', views.JSON_CurrentSensors, name="CurrentSensors"),
    url(r'^minute/current/$', views.JSON_CurrentMinuteData, name="CurrentMinuteData"),
    url(r'^hour/current/$', views.JSON_CurrentHourData, name="CurrentHourData"),
    url(r'^day/current/$', views.JSON_CurrentDayData, name="CurrentDayData"),
    url(r'^month/current/$', views.JSON_CurrentMonthData, name="CurrentMonthData"),
    url(r'^year/current/$', views.JSON_CurrentYearData, name="CurrentYearData"),

    url(r'^sensors/all$', views.JSON_allsensors, name="jsonsensordata"), #used for testing
    url(r'^minute/all$', views.JSON_allminutedata, name='jsonminutedata'), #used for testing
	
    url(r'^minute/(?P<householdid>[0-9]*)/$', views.JSON_minuteusagehouse, name='minuteusehousehold'),
    url(r'^hour/(?P<householdid>[0-9]*)/$', views.JSON_hourusagehouse, name='hourusehouse'),
    url(r'^day/(?P<householdid>[0-9]*)/$', views.JSON_dayusagehouse, name='dayusehouse'),
    url(r'^month/(?P<householdid>[0-9]*)/$', views.JSON_monthusagehouse, name='monthusehouse'),
    url(r'^year/(?P<householdid>[0-9]*)/$', views.JSON_yearusagehouse, name='yearusehouse'),

    url(r'^changeHouse/$', views.ChangeHouse, name="changehouse"),
    url(r'^addHouse/$', views.addHouse, name="addhouse"),
]