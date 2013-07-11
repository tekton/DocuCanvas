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
        print request.POST
        poll_form = PollForm(request.POST, instance=poll)
        formset = PollItemFormset(request.POST, instance=poll)
        if poll_form.is_valid() and formset.is_valid():
            p = poll_form.save()
            b = 0
            for a in request.POST.getlist('pollitem_set-TOTAL_FORMS'):
                if(int(a) > b):
                    b=a
            for i in range(0, int(b)):
                text = 'pollitem_set-' + str(i) + '-item'
                value = request.POST[text]
                item = PollItem(added_by=request.user, item=value, poll=poll)
                try:
                    item.save()
                except Exception, e:
                    print e
            print 'saving form'
            return redirect('polls.views.poll_overview', p.id)
        else:
            print poll_form.errors
            print formset.errors
    else:
        formset = PollItemFormset(instance=poll)

    poll_form = PollForm(instance=poll, auto_id=False)
    return render_to_response("polls/poll_form.html", {'poll': poll, 'formset': formset, "poll_form": poll_form, "projects": projects}, context_instance=RequestContext(request))


def poll_overview(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print e
    try:
        items = PollItem.objects.filter(poll=poll).order_by('-votes')
    except Exception, e:
        print e
    try:
        myuser = PollUser.objects.filter(poll=poll).filter(user=request.user)
    except Exception, e:
        print e
    return render_to_response("polls/poll_view.html", {'poll': poll, 'items': items, 'myuser': myuser}, context_instance=RequestContext(request))


def vote(request, poll_id):
    if request.method == 'POST':
        item_id = request.POST['item']
        try:
            mypoll = Poll.objects.get(pk=poll_id)
            myuser = PollUser.objects.filter(poll=mypoll)
        except Exception, e:
            print e
        try:
            user = myuser.objects.get(user=request.user)
        except Exception, e:
            user = PollUser(poll=mypoll, user=request.user)
        if user.voted == 0:
            try:
                item = PollItem.objects.get(pk=int(item_id))
                item.votes += 1
                item.save()
            except Exception, e:
                print e
    return redirect('polls.views.poll_overview', poll_id)
