from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'meta/new$', 'issues.views.meta_issue_form'),
    (r'meta/(\d+)/edit$', 'issues.views.meta_issue_form'),
    (r'(\d+)/edit', 'issues.views.edit'),
    (r'new/(\d+)', 'issues.views.issue_form_project'),
    (r'new', 'issues.views.issue_form'),
    (r'assign', 'issues.views.assign'),
    (r'set_bug_state', 'issues.views.set_bug_state'),
    (r'subscribe', 'issues.views.subscribe'),
    (r'pin/(\d+)$', 'issues.views.pin'),
    (r'advsearch', 'issues.views.issue_search_advanced'),
    (r'search', 'issues.views.issue_search_simple'),
    (r'comment/([A-Za-z0-9_\.-]+)', 'issues.views.submit_comment'),
    (r'([A-Za-z0-9_\.-]+)', 'issues.views.issue_overview'),
)
