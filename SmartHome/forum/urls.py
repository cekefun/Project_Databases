from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepageForum, name='homepageForum'),
    url(r'^(?P<wallname>[a-zA-Z0-9_]*)/$', views.showWall, name='showWall'),
    url(r'^(?P<wallname>[a-zA-Z0-9_]*)/addMessage/$', views.addMessage, name="addMessage")

]