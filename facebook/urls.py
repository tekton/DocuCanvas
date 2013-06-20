from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login$', 'facebook.views.facebook_login'),
)