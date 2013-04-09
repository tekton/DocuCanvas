from django.conf.urls.defaults import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'test',  'boards.views.TestIndex'),
    (r'^$', 'boards.views.index'),
    (r'new_board', 'boards.views.boards_form'),
    (r'new_note', 'boards.views.boards_note_form'),
    (r'new_node', 'boards.views.boards_node_form'),
)
