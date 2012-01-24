from django.conf.urls.defaults import *


urlpatterns = patterns('admin.views',
    #url for putting read  actions
    
    #url(r'^(#[a-zA-Z_])*$', 'index'),
    #url(r'^(?P<id>\d+)/$', 'index'),
    #url(r'^edit/(?P<id>\d+)/$', 'edit'),
    #url(r'^edit/(?P<id>\d+)/(?P<save>save)/$', 'edit'),
    
    
    url(r'^$', 'index_1'),
    url(r'^(?P<id>\d+)/$', 'delete_1'),
    url(r'^edit/(?P<id>\d+)/$', 'edit_1'),
    url(r'^edit/(?P<id>\d+)/(?P<save>save)/$', 'edit_1'),
)