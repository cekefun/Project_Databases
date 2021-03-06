from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.indexPage, name='indexpage'),
	url(r'^sensors/$', views.sensors, name='sensors'),
	url(r'^minute/$', views.minuteusage, name ='minuteuse'),
    url(r'^hour/$', views.hourlyusage, name='hourlyuse'),
    url(r'^day/$', views.dailyusage, name='dailyuse'),
    url(r'^week/$', views.weeklyusage, name='weeklyusage'),
    url(r'^month/$', views.monthlyusage, name='monthlyuse'),
    url(r'^year/$', views.yearlyusage, name='yearlyuse'),

    url(r'^sensors/updateSensor/$', views.Update_sensordata, name='updateSensordata'),
    url(r'^sensors/addSensor/$', views.Add_newSensor, name="addNewSensor"),
    url(r'^sensors/deleteSensor/$', views.Delete_sensor, name="deleteSensor"),
    url(r'^sensors/currentTitles/$', views.CurrentTitleSensors, name="currentTitleSensors"),
    url(r'^sensors/comments/$', views.commentsPage, name="commentspage"),
    url(r'^sensors/comments/addComment/$', views.addCommentSensor, name="addCommentSensor"),
    url(r'^sensors/usageSensors/$', views.JSON_usageSensors, name="JSONusageSensors"),
    
    url(r'^sensors/current/$', views.JSON_CurrentSensors, name="CurrentSensors"),
    url(r'^minute/current/$', views.JSON_CurrentMinuteData, name="CurrentMinuteData"),
    url(r'^hour/current/$', views.JSON_CurrentHourData, name="CurrentHourData"),
    url(r'^day/current/$', views.JSON_CurrentDayData, name="CurrentDayData"),
    url(r'^month/current/$', views.JSON_CurrentMonthData, name="CurrentMonthData"),
    url(r'^year/current/$', views.JSON_CurrentYearData, name="CurrentYearData"),
    url(r'^week/currentTotals/$', views.JSON_CurrentWeekDataTotals, name="CurrentWeekDataTotals"),

    url(r'^sensors/all/$', views.JSON_allsensors, name="jsonsensordata"), #used for testing
    url(r'^minute/all/$', views.JSON_allminutedata, name='jsonminutedata'), #used for testing
    url(r'^minute/currentMinute/$', views.JSON_CurrentMinute, name="CurrentMinute"),
    url(r'^hour/lastHour/$', views.JSON_LastHour, name="LastHour"),
    url(r'^hour/partialCurrent/$', views.JSON_partialCurrentHour, name="partialCurrentHour"),
    # url(r'^day/lastDay/$', views.JSON_LastDay, name="LastDay"),
    
    url(r'^minute/(?P<householdid>[0-9]*)/$', views.JSON_minuteusagehouse, name='minuteusehousehold'),
    url(r'^hour/(?P<householdid>[0-9]*)/$', views.JSON_hourusagehouse, name='hourusehouse'),
    url(r'^day/(?P<householdid>[0-9]*)/$', views.JSON_dayusagehouse, name='dayusehouse'),
    url(r'^month/(?P<householdid>[0-9]*)/$', views.JSON_monthusagehouse, name='monthusehouse'),
    url(r'^year/(?P<householdid>[0-9]*)/$', views.JSON_yearusagehouse, name='yearusehouse'),
    url(r'^sensors/comments/(?P<sensorID>[0-9]*)/$', views.JSON_commentssensor, name="commentssensor"),

    url(r'^settings/$', views.settingsPage, name="settings"),
    url(r'^settings/currentHouseholds/$', views.JSON_householdsprice, name="householdsprice"),
    url(r'^settings/updatePrice/$', views.updatePrice, name="updateprice"),
    url(r'^settings/changeHouse/$', views.changeCurrentHouse, name="changecurrenthouse"),
    url(r'^settings/changeLanguage/$', views.changeLanguage, name="changeLanguage"),

    url(r'^changeHouse/$', views.ChangeHouse, name="changehouse"),
    url(r'^addHouse/$', views.addHouse, name="addhouse"),
    url(r'^about/$', views.aboutPage, name="about"),
    url(r'^status/$', views.JSON_status, name="status"),

    url(r'^status/neighbourhood/$', views.powerOutageNeighbourhood, name="poweroutage_neighbourhood"),
    url(r'^status/powerSensors/$', views.powerOutageSensors, name="poweroutage_sensors"),
    url(r'^blackouts/$', views.historyOutages, name="historyOutages"),
]