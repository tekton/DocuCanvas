from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'pages.views.main'),
)
