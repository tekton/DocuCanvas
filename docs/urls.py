from django.conf.urls import *

urlpatterns = patterns('',
    (r'^(.*)$', 'docs.views.main'),
)
