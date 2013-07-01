from django.conf.urls import *

urlpatterns = patterns('',
    (r'^login$', 'facebook.views.facebook_login'),
)