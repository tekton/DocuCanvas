from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'^$', 'projects.views.home'),
    (r'names', 'projects.views.CodeNames'),
    (r'new', 'projects.views.project_form'),
    (r'(\d+)/edit', 'projects.views.edit'),
    (r'([A-Za-z0-9_\.-]+)', 'projects.views.project_overview'),
)
