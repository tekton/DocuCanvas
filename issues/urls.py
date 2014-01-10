from django.conf.urls import *

'''
    these all assume http[s]://URI/issue/ as the base
'''

urlpatterns = patterns('',
    #(r'set_issue_start_and_end_dates', 'issues.views.set_issue_start_and_end_dates'),
    (r'meta/new$', 'issues.views.meta_issue_form'),
    (r'meta/(\d+)/stats', 'issues.views.meta_issue_stats'),
    (r'meta/(\d+)/edit$', 'issues.views.meta_issue_form'),
    (r'meta/(\d+)', 'issues.views.meta_issue_overview'),
    (r'(\d+)/edit', 'issues.views.edit'),
    (r'test_view', 'issues.views.testView'),
    (r'(\d+)/history', 'issues.views.history'),
    (r'new/(\d+)/(\d+)$', 'issues.views.issue_form_project_and_meta'),
    (r'new/(\d+)$', 'issues.views.issue_form_project'),
    (r'new', 'issues.views.issue_form'),
    (r'as/(\d+)/(\d+)$', 'issues.views.assign_to_user'),
    (r'assign/(\d+)/(\d+)$', 'issues.views.assign'),
    (r'assign/(\d+)$', 'issues.views.assign'),
    (r'unassigned$', 'issues.views.unassigned_issues'),
    (r'set_bug_state', 'issues.views.set_bug_state'),
    (r'subscribe/(\d+)/(\d+)$', 'issues.views.issueSubscribe'),
    (r'subscribe/(\d+)$', 'issues.views.subscribe'),
    (r'pin/(\d+)$', 'issues.views.pin'),
    (r'unlink', 'issues.views.unlink_issues'),
    (r'link', 'issues.views.issue_to_issue_link'),
    (r'advsearch$', 'issues.views.issue_search_advanced'),
    (r'advsearch/([A-Za-z0-9_\.-]+)$', 'issues.views.loadSearchResults'),
    (r'search', 'issues.views.issue_search_simple'),
    (r'comment/([A-Za-z0-9_\.-]+)', 'issues.views.submit_comment'),
    (r'edit_comment', 'issues.views.edit_comment'),
    (r'track', 'issues.views.trackIssues'),
    (r'overview', 'issues.views.overview'),
    (r'([A-Za-z0-9_\.-]+)', 'issues.views.issue_overview'),
)
