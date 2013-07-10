from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from polls.models import Poll, PollItem, PollUser
from polls.forms import PollForm, ItemForm


def new_poll(request):
    PollItemFormset = inlineformset_factory(Poll, PollItem, can_delete=False, extra=1)
    poll = Poll()
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        formset = PollItemFormset(request.POST, instance=poll)
        if poll_form.is_valid() and formset.is_valid():
            p = poll_form.save()
            formset.save()
            print 'saving form'
            return redirect('polls.views.poll_overview', p.id)
        else:
            print poll_form.errors
            print formset.errors
    else:
        formset = PollItemFormset(instance=poll)

    poll_form = PollForm(instance=poll, auto_id=False)
    return render_to_response("polls/poll_form.html", {'formset': formset, "poll_form": poll_form, "projects": projects}, context_instance=RequestContext(request))


def poll_view(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print e
    try:
        items = PollItem.objects.filter(poll=poll)
    except Exception, e:
        print e
    return render_to_response("polls/poll_view.html", {'poll': poll, 'items': items}, context_instance=RequestContext(request))