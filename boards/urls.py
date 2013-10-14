from django.conf.urls import *

'''
    these all assume http[s]://URI/board/ as the base
'''

urlpatterns = patterns('',
    (r'test',  'boards.views.boards'),
    (r'^$', 'boards.views.index'),
    (r'new_board', 'boards.views.boards_form'),
    (r'new_note', 'boards.views.boards_note_form'),
    (r'new_node', 'boards.views.boards_node_form'),
    (r'boards', 'boards.views.boards'),
    url(r'board_edit/(\d+)/$', 'boards.views.board_edit', name='board_url_edit'),
    url(r'board_display/(\d+)/$', 'boards.views.board_display', name='board_url_display'),
)
