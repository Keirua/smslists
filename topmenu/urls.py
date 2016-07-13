from django.conf.urls import url
from . import views
from django.contrib import admin
app_name = "topmenu"
urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^plivo_endpoint/$', views.plivo_endpoint, name='plivo_endpoint')
	url(r'^menu_2/$', views.menu_2, name='menu_2'), # name arg used for reverse URL lookup
	url(r'^/listings/(?P<category>\w+)/', views.listings, name='listings'),
	url(r'^/listings/(?P<category>\w+)/(?P<id>\d+)/', views.listing_detail, name='listing_detail')
	]




"""
	urlpatterns = [
    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}),
]
url(r'^/listings/(?P<category_name>\w+)/(?P<id>\d+)/'
"""