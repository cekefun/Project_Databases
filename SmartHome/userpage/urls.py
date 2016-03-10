from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.indexpage, name='indexpage'),
	url(r'^sensors/', views.sensors, name='sensors'),
	url(r'^minute/', views.minuteusage, name ='minuteuse'),
    url(r'^daily/', views.dailyusage, name='dailyuse'),
    url(r'^monthly/', views.monthlyusage, name='monthlyuse')
]