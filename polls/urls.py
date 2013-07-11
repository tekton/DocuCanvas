from django.conf.urls import *

urlpatterns = patterns('',
    (r'^new/', 'polls.views.new_poll'),
    (r'^overview/([A-Za-z0-9_\.-]+)$', 'polls.views.poll_overview'),
    (r'^vote/([A-Za-z0-9_\.-]+)$', 'polls.views.vote'),
)
