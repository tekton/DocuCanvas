from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'new', 'daily_reports.views.daily_report_form'),
    # (r'([A-Za-z0-9_\.-]+)', 'daily_reports.views.daily_report_overview'),
)
