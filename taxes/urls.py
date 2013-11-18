from django.conf.urls import *

'''
    these all assume http[s]://URI/issue/ as the base
'''

urlpatterns = patterns('',
    (r'projects$', 'taxes.views.submitProjectForm'),
    (r'supplies$', 'taxes.views.submitSupplyForm'),
    (r'contract$', 'taxes.views.submitContractForm'),
    (r'editprojectlist/([A-Za-z0-9_\.-]+)', 'taxes.views.editProjectForm'),
    (r'editsupplylist/([A-Za-z0-9_\.-]+)', 'taxes.views.editSupplyForm'),
    (r'editcontractlist/([A-Za-z0-9_\.-]+)', 'taxes.views.editContractForm'),
    (r'deleteInstance/([A-Za-z0-9_\.-]+)', 'taxes.views.deleteProjectListInstance'),
    (r'information$', 'taxes.views.createChecklist'),
    (r'information/([A-Za-z0-9_\.-]+)$', 'taxes.views.createChecklist'),
    (r'viewinfo/([A-Za-z0-9_\.-]+)$', 'taxes.views.viewInfoChecklist'),
)
