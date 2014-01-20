from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'^new$', 'sprints.views.createSprint'),
    (r'^(\d+)$', 'sprints.views.viewSprint'),
    (r'^$', 'sprints.views.viewAll'),
    (r'^assign/(\d+)$', 'sprints.views.assignSprint'),
    (r'^assign/(\d+)/(\d+)$', 'sprints.views.assignSprint'),
    (r'^auto$', 'sprints.views.autoCreateSprints'),
    (r'^widget$', 'sprints.views.loadWidget'),
)