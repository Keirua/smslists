""" Default urlconf for smscl """

from django.conf.urls import include, patterns, url
from django.contrib import admin
admin.autodiscover()


def bad(request):
    """ Simulates a server error """
    1 / 0 #what does this mean

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smscl.views.home', name='home'), #what is name for?
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^topmenu/', include('topmenu.urls')),
    url(r'^bad/$', bad), #need to update this for django 1.10?
)

