from django.conf.urls import *

'''
    these all assume http[s]://URI/issue/ as the base
'''

urlpatterns = patterns('',
    (r'^projects$', 'taxes.views.submitProjectForm'),
    (r'^supplies$', 'taxes.views.submitSupplyForm'),
    (r'^contract$', 'taxes.views.submitContractForm'),
)
