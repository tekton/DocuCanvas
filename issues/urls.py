from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'new', 'issues.views.issue_form'),
    (r'subscribe', 'issues.views.subscribe'),
    (r'comment/([A-Za-z0-9_\.-]+)', 'issues.views.submit_comment'),
    (r'pin', 'issues.views.pin'),
    (r'([A-Za-z0-9_\.-]+)', 'issues.views.issue_overview'),
)
