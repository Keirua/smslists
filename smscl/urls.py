""" Default urlconf for smscl """

from django.conf.urls import include, patterns, url
from django.contrib import admin
admin.autodiscover()


def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smscl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include(smscl.apps.main.urls)),
    url(r'^bad/$', bad),
)

