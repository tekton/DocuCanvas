from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'search.views.search'),
)