from django.conf.urls import *

'''
    these all assume http[s]://URI/reports/ as the base
'''

urlpatterns = patterns('',
                       url(r'edit/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})', 'daily_reports.views.edit_report'),
                       url(r'edit$', 'daily_reports.views.edit_report'),
                       url(r'editglobal/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})', 'daily_reports.views.edit_global_report'),
                       url(r'editglobal$', 'daily_reports.views.edit_global_report'),
                       url(r'view/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})', 'daily_reports.views.view_reports'),
                       url(r'view$', 'daily_reports.views.view_reports'),
                       url(r'^$', 'daily_reports.views.index'),
                       #url(r'view_all', 'daily_reports.views.view_reports_wip'),
                       url(r'report_selection', 'daily_reports.views.report_selection'),
                       url(r'view_all/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/$', 'daily_reports.views.view_reports_wip'),
                       url(r'summary/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})/([A-Za-z0-9_\.-]+)/$', 'daily_reports.views.report_summary'),
                       url(r'^report_group$', 'daily_reports.views.setup_report_group'),
                       url(r'^edit_group/([A-Za-z0-9_\.-]+)/$', 'daily_reports.views.edit_group'),
                       url(r'^request_summary$', 'daily_reports.views.request_report_summary'),
                       url(r'^report_redirect$', 'daily_reports.views.reportRedirect'),
                       )
