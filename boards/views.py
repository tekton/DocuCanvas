from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import *
from boards.models import *
from issues.models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse


@login_required
def TestIndex(request):
    return render_to_response("test_templates/test_board.html", {}, context_instance=RequestContext(request))


@login_required
def boards_form(request):
    if request.method == 'POST':
        board = Board()
        form = BoardForm(request.POST, request.FILES, instance=board)

        if form.is_valid():
            try:
                board = form.save()
                return redirect('board_url_edit', board.id)
            except Exception, e:
                print e
    else:
        form = BoardForm()

    return render_to_response('boards/boards_form.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def boards_note_form(request):
    if request.method == 'POST':
        boardNote = BoardNote()
        form = BoardNoteForm(request.POST, instance=boardNote)

        if form.is_valid():
            try:
                boardNote = form.save()
                return HttpResponseRedirect('boards/new_node')
            except:
                print 'unable to save note'

    else:
        form = BoardNoteForm()

    return render_to_response('boards/board_note_form.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def boards_node_form(request):
    if request.method == 'POST':
        boardNode = BoardNode()
        form = BoardNodeForm(request.POST, instance=boardNode)

        if form.is_valid():
            try:
                boardNode = form.save()
                return HttpResponseRedirect('boards/new_node')
            except:
                print 'unable to save node'

    else:
        form = BoardNodeForm()

    return render_to_response('boards/board_node_form.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def index(request):
    board_nodes = Board.objects.all()
    board_node_count = BoardNode.objects.count()
    context = {'board_nodes': board_nodes, 'board_node_count': board_node_count}
    return render_to_response('boards/index.html', context)


@login_required
def boards(request):
    boards = Board.objects.all()
    context = {'boards': boards}
    return render_to_response('boards/boards.html', context)


@login_required
def board_edit(request, board_id):
    board_nodes = BoardNode.objects.all()
    board_notes = BoardNote.objects.all()
    issues = Issue.objects.all()
    print "Submitting board..."
    nodeId = request.POST.get('id', "")
    nodeType = request.POST.get('nodeType', "")
    print nodeType
    if nodeType == 'note':
        if request.method == 'POST':
            if nodeId:
                boardNode = BoardNode.objects.get(pk=nodeId)
            else:
                boardNode = BoardNode()
            boardNote = BoardNote()
            form = BoardNoteForm(request.POST, instance=boardNote)
            if form.is_valid():
                try:
                    boardNote.user = request.user
                    boardNote = form.save()
                    nodeLinkId = boardNote.id
                    print nodeLinkId
                    boardNode.x = request.POST.get('x', '')
                    boardNode.y = request.POST.get('y', '')
                    boardNode.nodeLink = nodeLinkId
                    boardNode.nodeType = request.POST.get('nodeType', '')
                    boardNode.board = Board.objects.get(pk=board_id)
                    boardNode.save()

                except Exception, e:
                    print e
                    print 'unable to save node'
                    print form.errors
            else:
                print form.errors

        else:
            form = BoardNoteForm()
    else:
        print 'IT\'S PROBABLY AN ISSUE'
        if request.method == 'POST':
            if nodeId:
                boardNode = BoardNode.objects.get(pk=nodeId)
            else:
                boardNode = BoardNode()

            form = BoardNodeForm(request.POST, instance=boardNode)
            if form.is_valid():
                try:
                    boardNode = form.save()
                except Exception, e:
                    print e
                    print 'unable to save node'
                    print form.errors
            else:
                print form.errors

        else:
            form = BoardNodeForm()
    try:
        p = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404
    return render_to_response('boards/board_edit.html', {'board': p, 'form': form, 'board_nodes': board_nodes, 'board_notes': board_notes, 'issues': issues}, context_instance=RequestContext(request))


@login_required
def board_display(request, board_id):
    board_nodes = BoardNode.objects.all()
    board_notes = BoardNote.objects.all()
    issues = Issue.objects.all()
    try:
        p = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        raise Http404
    return render_to_response('boards/board_display.html', {'board': p, 'board_nodes': board_nodes, 'board_notes': board_notes, 'issues': issues}, context_instance=RequestContext(request))
