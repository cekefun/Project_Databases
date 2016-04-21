from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register, name='dailyuse'),
    url(r'^Login/$', views.login, name='login')
    #url(r'^Registered', views.register, name='Registerer')
]
