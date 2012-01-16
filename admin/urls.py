from django.conf.urls.defaults import *


urlpatterns = patterns('admin.views',
    #url for putting read  actions
    url(r'^$', 'index'),
    url(r'^(?P<id>\d+)/$', 'index'),
    url(r'^edit/(?P<id>\d+)/$', 'edit'),
    url(r'^edit/(?P<id>\d+)/save/$', 'edit'),
)