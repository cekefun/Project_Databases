from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.loginpage, name='dailyuse'),
    #url(r'^Registered', views.register, name='Registerer')
]

