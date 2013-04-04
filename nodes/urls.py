# Create your views here.
from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'test',  'bugs.views.TestIndex'),
)