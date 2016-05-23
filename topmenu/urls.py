from django.conf.urls import url
from . import views
from django.contrib import admin
app_name = "topmenu"
urlpatterns = [
	url(r'^$', views.index, name='index'),
	]