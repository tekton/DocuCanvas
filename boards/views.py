from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import BoardNodeForm, BoardNoteForm, BoardsForm


def TestIndex(request):
    return render_to_response("test_templates/test_board.html", {}, context_instance=RequestContext(request))


def boards_form(request):
    form = BoardsForm()
    return render_to_response("boards/boards_form.html", {'form': form}, context_instance=RequestContext(request))


def boards_note_form(request):
    form = BoardNoteForm()
    return render_to_response("boards/board_note_form.html", {'form': form}, context_instance=RequestContext(request))


def boards_node_form(request):
    form = BoardNodeForm()
    return render_to_response("boards/board_node_form.html", {'form': form}, context_instance=RequestContext(request))