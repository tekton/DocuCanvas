from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
from boards.models import *


def TestIndex(request):
    return render_to_response("test_templates/test_board.html", {}, context_instance=RequestContext(request))


def boards_form(request):
    if request.method == 'POST':
        board = Board()
        form = BoardForm(request.POST, instance=board)

        if form.is_valid():
            try:
                board = form.save()
            except:
                print 'unable to save board'
    else:
        form = BoardForm()

    return render_to_response('boards/boards_form.html', {'form': form}, context_instance=RequestContext(request))


def boards_note_form(request):
    if request.method == 'POST':
        boardNote = BoardNote()
        form = BoardNoteForm(request.POST, instance=boardNote)

        if form.is_valid():
            try:
                boardNote = form.save()
            except:
                print 'unable to save note'

    else:
        form = BoardNoteForm()

    return render_to_response('boards/board_note_form.html', {'form': form}, context_instance=RequestContext(request))


def boards_node_form(request):
    if request.method == 'POST':
        boardNode = BoardNode()
        form = BoardNodeForm(request.POST, instance=boardNode)

        if form.is_valid():
            try:
                boardNode = form.save()
            except:
                print 'unable to save node'

    else:
        form = BoardNodeForm()

    return render_to_response('boards/board_node_form.html', {'form': form}, context_instance=RequestContext(request))
