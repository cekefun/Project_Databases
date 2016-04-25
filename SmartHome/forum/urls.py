from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepageForum, name='homepageForum'),
    url(r'^(?P<wallname>.*)/$', views.showWall, name='showWall'),

]