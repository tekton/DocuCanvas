from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    #(r'projects/(\d+)/new_instance', 'checklists.views.new_instance'),
    (r'checklist_instance_new/(\d+)', 'checklists.views.new_instance'),
    (r'project/(\d+)', 'checklists.views.project_checklists'),
    (r'new/(\d+)', 'checklists.views.checklist_form_project'),
    #(r'(\d+)/edit', 'checklists.views.edit'),
    (r'instance/(\d+)', 'checklists.views.instance_edit'),
    #(r'overview/(\d+)', 'checklists.views.overview'),
    (r'(\d+)', 'checklists.views.checklist_edit'),
)
