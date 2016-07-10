from django.conf.urls import url
from . import views
from django.contrib import admin
app_name = "topmenu"
urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^plivo_endpoint/$', views.plivo_endpoint, name='plivo_endpoint')
	url(r'^menu_2/$', views.menu_2, name='menu_2') # name arg used for reverse URL lookup
	url(r'^/listings/for_sale/(?P<id>\d+)/', views.listings, {'category':'for_sale'}, name='listings_for_sale')
	url(r'^/listings/wanted/(?P<id>\d+)/', views.listings, {'category':'wanted'}, name='listings_wanted')
	url(r'^/listings/jobs/(?P<id>\d+)/', views.listings, {'category':'jobs'}, name='listings_jobs')
	url(r'^/listings/announcements/(?P<id>\d+)/', views.listings, {'category':'announcements'}, name='listings_announcements')
	]





	urlpatterns = [
    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}),
]
url(r'^/listings/(?P<category_name>\w+)/(?P<id>\d+)/'