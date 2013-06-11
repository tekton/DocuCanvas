from django.conf.urls import *

'''
    these all assume http[s]:/notifications/
'''

urlpatterns = patterns('',
    (r'new', 'notifications.views.notification_form'),
)
