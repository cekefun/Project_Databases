from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^uploaded', views.upload, name='uploaded'),
    url(r'^MY_FILE.csv', views.uploadPage, name='upload')
]
