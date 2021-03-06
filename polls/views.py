from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from polls.models import Poll, PollItem, PollUser, UserVoteItem
from polls.forms import PollForm, ItemForm
from datetime import date, timedelta


@login_required
def new_poll(request):
    PollItemFormset = inlineformset_factory(Poll, PollItem, can_delete=False, extra=1)
    poll = Poll()
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
    if request.method == 'POST':
        print(request.POST)
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
                    print(e)
            poll.total_items = b
            poll.save()
            print('saving form')
            return redirect('socialplatform.views.notify_new_poll', p.id)
        else:
            print(poll_form.errors)
            print(formset.errors)
    else:
        formset = PollItemFormset(instance=poll)

    poll_form = PollForm(instance=poll, auto_id=False)

    

    return render_to_response("polls/poll_form.html", {'poll': poll, 'formset': formset, "poll_form": poll_form, "projects": projects}, context_instance=RequestContext(request))


@login_required
def poll_overview(request, poll_id):
    
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print(e)
    
    after = True
    time_difference = date.today() - poll.end_date

    if time_difference.total_seconds() > 0:
        after = False

    #today = date.today() #2013-07-15
    #end_date = poll.end_date #07/18/2013
    #today_year = int(today[:4])
    #today_month = int(today[5:7])
    #today_day = int(today[8:])
    #end_year = int(end_date[:4])
    #end_month = int(end_date[5:7])
    #end_day = int(end_date[8:])
    #after = True
    #if today_year > end_year:
    #    after = False
    #elif today_year == end_year and today_month > end_month:
    #    after = False
    #elif today_year == end_year and today_month == end_month and today_day > end_day:
    #    after = False
    #else:
    #    after = True
    

    if after:

        try:
            projects = Project.objects.all()
        except Exception, e:
            raise e
        try:
            items = PollItem.objects.filter(poll=poll).order_by('id')
        except Exception, e:
            print(e)
        try:
            uservoteitems = UserVoteItem.objects.filter(poll=poll).filter(user=request.user).filter(voted=True)
        except Exception, e:
            print(e)

        votes_allowed = poll.max_votes - uservoteitems.count()
        

        usernotvoteitems = []

        for item in items:
            try:
                user_item = UserVoteItem.objects.filter(user=request.user).filter(item=item)
            except Exception, e:
                print(e)
            if user_item.count() > 0:
                for myitem in user_item:
                    usernotvoteitems.append(myitem)
            else:
                new_vote_item = UserVoteItem(user=request.user, item=item, voted=False, poll=poll)
                new_vote_item.save()
                usernotvoteitems.append(new_vote_item)
    
    
        sup = True
    
        if uservoteitems.count() >= poll.max_votes:
            sup = False

        most_votes = 0
        for item in items:
            if item.votes > most_votes:
                most_votes = item.votes

        
        return render_to_response("polls/poll_view.html", {'poll': poll, 'items': items, 'votes_allowed': votes_allowed, 'myuser': request.user, 'sup': sup, 'projects': projects, 'usernotvoteitems': usernotvoteitems, 'most_votes': most_votes, 'uservoteitems' : uservoteitems}, context_instance=RequestContext(request))
    return redirect("polls.views.poll_results", poll_id)

@login_required
def end_poll(request, poll_id):
    if request.method == 'POST':
        try:
            mypoll = Poll.objects.get(pk=poll_id)
        except Exception, e:
            print(e)
        try:
            mypoll.end_date = date.today()-timedelta(days=1)
            print(mypoll.end_date)
            mypoll.save()
        except Exception, e:
            print(e)
    return redirect('polls.views.poll_overview', poll_id)


@login_required
def extend_poll(request, poll_id):
    try:
        mypoll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print(e)
    if request.method == 'POST':
        try:
            mypoll.end_date = request.POST['end_date']
            print(mypoll.end_date)
            mypoll.save()
        except Exception, e:
            print(e)
        return redirect('polls.views.poll_overview', poll_id)
    return render_to_response("polls/extend_poll.html", {'poll': mypoll}, context_instance=RequestContext(request))



def poll_results(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print(e)
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    try:
        items = PollItem.objects.filter(poll=poll).order_by('-votes')
    except Exception, e:
        print(e)
    try:
        myuser = PollUser.objects.filter(poll=poll).filter(user=request.user)
    except Exception, e:
        print(e)
    sup = True
    if uservoteitems.count() <= mypoll.max_votes:
    #if myuser.count() != 0:
        sup = False
    most_votes = 0
    for item in items:
        if item.votes > most_votes:
            most_votes = item.votes
        
    return render_to_response("polls/poll_results.html", {'poll': poll, 'items': items, 'myuser': myuser, 'sup': sup, 'projects': projects, 'most_votes': most_votes}, context_instance=RequestContext(request))


@login_required
def add_items(request, poll_id):
    PollItemFormset = inlineformset_factory(Poll, PollItem, can_delete=False, extra=1)
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        return redirect('polls.views.poll_overview', poll_id)
    if request.method == 'POST':
        formset = PollItemFormset(request.POST, instance=poll)
        if formset.is_valid():
            b = 0
            for a in request.POST.getlist('pollitem_set-TOTAL_FORMS'):
                if(int(a) > b):
                    b=a
            for i in range(0, (int(b) - poll.total_items)):
                text = 'pollitem_set-' + str(i) + '-item'
                value = request.POST[text]
                item = PollItem(added_by=request.user, item=value, poll=poll)
                try:
                    item.save()
                except Exception, e:
                    print(e)
            poll.total_items = b
            poll.save()
            print('saving form')
            return redirect('polls.views.poll_overview', poll_id)
        else:
            print(poll_form.errors)
            print(formset.errors)
    else:
        formset = PollItemFormset(instance=poll)

    return render_to_response("polls/add_items.html", {'poll': poll, 'formset': formset, "projects": projects}, context_instance=RequestContext(request))

@login_required
def undo_vote(request, poll_id):
    try:
        mypoll = Poll.objects.get(pk=poll_id)
    except Exception, e:
        print(e)
    try:
        items = UserVoteItem.objects.filter(poll=mypoll).filter(user=request.user).filter(voted=True)
    except Exception, e:
        print(e)
    print(items.count())
    if items.count() > 0:
        try:
            for item in items:
                
                if item.voted:

                    item.item.votes -= 1
                    item.voted = False
                    item.save()
                    item.item.save()
        except Exception,e :
            print(e)
    return redirect('polls.views.poll_overview', poll_id)       
    



@login_required
def vote(request, poll_id):
    print(request.POST)
    if request.method == 'POST':
        item_id = request.POST['item']
        try:
            mypoll = Poll.objects.get(pk=poll_id) 
            uservoteitems = UserVoteItem.objects.filter(poll=mypoll).filter(user=request.user).filter(voted=True)       
        except Exception, e:
            print(e)
        
        if uservoteitems.count() <= mypoll.max_votes:

            try:
                newuser = PollUser(user=request.user, poll=mypoll)
                items = PollItem.objects.filter(poll=mypoll)
                for item in items:

                    if str(item.id) in request.POST:
                        new_vote_item = UserVoteItem.objects.filter(item=item).filter(user=request.user)
                        for thing in new_vote_item:
                            if not thing.voted:
                                thing.voted=True
                                thing.save()
                                item.votes += 1
                                item.save()
                newuser.save()   
            except Exception, e:
                print(e)

    

    return redirect('polls.views.poll_overview', poll_id)




@login_required
def all_polls(request):
    try:
        polls = Poll.objects.all()
    except Exception, e:
        print(e)
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    return render_to_response("polls/all.html", {'polls': polls, 'projects': projects}, context_instance=RequestContext(request))