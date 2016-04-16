from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^Family', views.upload_json, name='uploadFam')
]
