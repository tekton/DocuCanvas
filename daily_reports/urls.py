from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/reports/ as the base
'''

urlpatterns = patterns('',
    url(r'edit', 'daily_reports.views.edit_report_today'),
    # (r'([A-Za-z0-9_\.-]+)', 'daily_reports.views.daily_report_overview'),
)
