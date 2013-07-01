from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^getAccessToken$', 'facebook.views.getAccessToken'),
    (r'^connect$', 'facebook.views.facebookConnect')
)