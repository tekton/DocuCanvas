from django.conf.urls import *

'''
    these all assume http[s]:/newsfeed/ as the base
'''

urlpatterns = patterns('',
    (r'([A-Za-z0-9_\.-]+)', 'newsfeed.views.newsfeed_action'),
)
