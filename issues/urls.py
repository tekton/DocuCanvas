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
    (r'assign/(\d+)/(\d+)$', 'issues.views.assign'),
    (r'assign/(\d+)$', 'issues.views.assign'),
    (r'unassigned$', 'issues.views.unassigned_issues'),
    (r'set_bug_state', 'issues.views.set_bug_state'),
    (r'subscribe/(\d+)$', 'issues.views.subscribe'),
    (r'pin/(\d+)$', 'issues.views.pin'),
    (r'unlink', 'issues.views.unlink_issues'),
    (r'link', 'issues.views.issue_to_issue_link'),
    (r'advsearch', 'issues.views.issue_search_advanced'),
    (r'search', 'issues.views.issue_search_simple'),
    (r'comment', 'issues.views.submit_comment'),
    (r'([A-Za-z0-9_\.-]+)', 'issues.views.issue_overview'),
)
