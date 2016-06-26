from django.conf.urls import url
from . import views
from django.contrib import admin
app_name = "topmenu"
urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^plivo_endpoint/$', views.plivo_endpoint, name='plivo_endpoint')
	url(r'^menu_2/$', views.menu_2,  name='menu_2') # name arg used for reverse URL lookup
	url(r'^listings/$', views.listings, name='listings')
	url(r'^wanted/$', views.wanted, name='wanted')
	url(r'^jobs/$', views.jobs, name='jobs')
	url(r'^announcements/$' views.announcements, name='announcements')
	]