from django.conf.url import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	]