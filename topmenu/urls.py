from django.conf.urls import url
import views

app_name = "topmenu"

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^menu_2/$', views.menu_2, name='menu_2'),
	# why isn't 'create_user' being passed to view and thus making create_user != its default value of none? 
	url(r'^menu_2/create_user/$', views.menu_2, name='menu_2/create_user'),
	url(r'^listings/(?P<category>\w+)/', views.listings, name='listings'),
	url(r'^session_flush/$', views.session_flush, name='session_flush'),

	# NOTE: category doesn't matter/superflous here, since listings have unique id's across categories anyway
	url(r'^listings/(?P<category>\w+)/(?P<id>\d+)/', views.listing_detail, name='listing_detail'),
	url(r'^post_subject_request/(?P<category>\w+)/', views.post_subject_request, name='post_subject_request'),
	url(r'^post_description_request/(?P<category>\w+)/', views.post_description_request, name='post_description_request'),
	url(r'^post_review/(?P<category>\w+)/', views.post_review, name='post_review'),
	url(r'^post_commit/(?P<category>\w+)/', views.post_commit, name='post_commit'),
	]
