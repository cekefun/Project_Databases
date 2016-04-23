from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='dailyuse'),
    url(r'^users/$', views.users, name='Users'),
    url(r'^users/updateAdmin/$', views.UpdateAdmin, name='Admin'),
    url(r'^report/$', views.reportpage, name='reppage'),
    url(r'^report/Reported/$', views.getreport, name='report'),
]

