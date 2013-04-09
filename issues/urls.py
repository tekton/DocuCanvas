from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'new', 'issues.views.issue_form'),
    (r'assign', 'issues.views.assign'),
    (r'subscribe', 'issues.views.subscribe'),
    (r'pin', 'issues.views.pin'),
    (r'comment/([A-Za-z0-9_\.-]+)', 'issues.views.submit_comment'),
    (r'([A-Za-z0-9_\.-]+)', 'issues.views.issue_overview'),
)
