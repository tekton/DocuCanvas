from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'^new$', 'sprints.views.createSprint'),
    (r'^(\d+)$', 'sprints.views.viewSprint'),
)