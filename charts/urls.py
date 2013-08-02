from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'^project/(\d+)/issues_chart', 'charts.views.issues_by_project_chart'),
    (r'^project/(\d+)/meta_issues_chart', 'charts.views.meta_issues_by_project'),
    (r'^projects_chart', 'charts.views.projects_chart'),
    (r'^users_chart', 'charts.views.users_chart'),
    (r'^user/unassigned_issues_chart', 'charts.views.unassigned_issues_chart'),
    (r'^user/(\d+)/issues_chart', 'charts.views.issues_by_user_chart'),
    (r'^test', 'charts.views.test'),
    (r'^$', 'charts.views.home'),
)
