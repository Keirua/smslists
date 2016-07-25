from django.conf.urls import url
import views

app_name = "topmenu"

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^plivo_endpoint/$', views.plivo_endpoint, name='plivo_endpoint')
	url(r'^menu_2/$', views.menu_2, name='menu_2'), # name arg used for reverse URL lookup
	url(r'^listings/(?P<category>\w+)/', views.listings, name='listings'),

	# NOTE: category doesn't matter/superflous here, since listings have unique id's across categories anyway
	url(r'^listings/(?P<category>\w+)/(?P<id>\d+)/', views.listing_detail, name='listing_detail'),
	url(r'^post_subject_request/(?P<category>\w+)/', views.post_subject_request, name='post_subject_request'),
	url(r'^post_description_request/(?P<category>\w+)/', views.post_description_request, name='post_description_request'),
	url(r'^post_review/(?P<category>\w+)/', views.post_review, name='post_review'),
	url(r'^post_commit/(?P<category>\w+)/', views.post_commit, name='post_commit'),
	]
