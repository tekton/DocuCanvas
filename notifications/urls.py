from django.conf.urls import *

'''
    these all assume http[s]:/notifications/
'''

urlpatterns = patterns('',
    (r'all', 'notifications.views.notifications'),
    (r'new', 'notifications.views.notification_form'),
    (r'mark_as_read', 'notifications.views.mark_as_read'),
)
