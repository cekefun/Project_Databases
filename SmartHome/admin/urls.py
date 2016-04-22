from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='dailyuse'),
    url(r'^users', views.users, name='Users')
]

