from django.conf.urls import *

'''
    these all assume http[s]:/newsfeed/ as the base
'''

urlpatterns = patterns('',
    (r'all', 'newsfeed.views.newsfeeds'),
    (r'([A-Za-z0-9_\.-]+)', 'newsfeed.views.newsfeed_action'),

)
