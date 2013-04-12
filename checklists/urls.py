from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'new/(\d+)', 'checklists.views.checklist_form_project'),
    (r'new', 'checklists.views.checklist_form_project'),
    (r'(\d+)/edit', 'checklists.views.edit'),
    (r'(\d+)', 'checklists.views.overview'),

)
