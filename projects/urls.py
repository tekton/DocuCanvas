from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'^$', 'projects.views.home'),
    (r'names', 'projects.views.CodeNames'),
    (r'new', 'projects.views.project_form'),
    (r'save_project_planner_item', 'projects.views.save_project_planner_item'),
    (r'save_project_planner_item_connection', 'projects.views.save_project_planner_item_connection'),
    (r'(\d+)/stats', 'projects.views.project_stats'),
    (r'(\d+)/edit', 'projects.views.edit'),
    (r'([A-Za-z0-9_\.-]+)', 'projects.views.project_overview'),

)
