from django.conf.urls import *

urlpatterns = patterns('',
    (r'^getAccessToken$', 'facebook.views.getAccessToken'),
    (r'^connect$', 'facebook.views.facebookConnect')
)