from django.conf.urls import *

urlpatterns = patterns('',
    (r'^new/', 'polls.views.new_poll'),
    (r'^overview/([A-Za-z0-9_\.-]+)$', 'polls.views.poll_overview'),
    (r'^vote/([A-Za-z0-9_\.-]+)$', 'polls.views.vote'),
    (r'^add/([A-Za-z0-9_\.-]+)$', 'polls.views.add_items'),
    (r'^$', 'polls.views.all_polls'),
    (r'^poll_results/([A-Za-z0-9_\.-]+)$', 'polls.views.poll_results'),
    (r'^end_poll/([A-Za-z0-9_\.-]+)$', 'polls.views.end_poll'),
    (r'^restart_poll/([A-Za-z0-9_\.-]+)$', 'polls.views.restart_poll')

)
