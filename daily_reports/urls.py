from django.conf.urls import *

'''
    these all assume http[s]://URI/reports/ as the base
'''

urlpatterns = patterns('',
    url(r'edit/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})' , 'daily_reports.views.edit_report'),
    url(r'edit$', 'daily_reports.views.edit_report'),
    url(r'editglobal/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})' , 'daily_reports.views.edit_global_report'),
    url(r'editglobal$', 'daily_reports.views.edit_global_report'),
    url(r'view/([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})' , 'daily_reports.views.view_reports'),
    url(r'view$', 'daily_reports.views.view_reports'),
)
