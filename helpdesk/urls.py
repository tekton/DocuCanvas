from django.conf.urls import *

urlpatterns = patterns('',
    (r'new', 'helpdesk.views.help_form'),
    (r'all', 'helpdesk.views.get_all'),
    (r'pending', 'helpdesk.views.get_pending'),
    (r'([A-Za-z0-9_\.-]+)', 'helpdesk.views.get_help'),
)
