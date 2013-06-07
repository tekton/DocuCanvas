from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projects.models import *
from projects.forms import *
from newsfeed.models import NewsFeedItem
from issues.models import *

@login_required
def home(request):
    '''
        need comments
    '''
    #issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
    issues = Issue.objects.filter(Q(assigned_to = request.user) & (Q(status = "active") | Q(status = "retest") | Q(status = "unverified") | Q(status__isnull=True))).order_by('-created')
    #pins = PinIssue.objects.select_related().filter(user=request.user)
    pins = Issue.objects.filter(pinissue__user=request.user).order_by('-created')
    subscribed = Issue.objects.filter(subscriptiontoissue__user=request.user).order_by('-created')
    newsfeeds = NewsFeedItem.objects.all().order_by('-id')[:20]
    #projects = Project.objects.filter(lead_developer=request.user).order_by('-created')
    projects = Project.objects.all()
    #subscribed = SubscriptionToIssue.objects.select_related().filter(user=request.user)
    return render_to_response("dashboard.html", {"issues": issues, "subscribed": subscribed, 
            "projects": projects, "pins": pins, "newsfeeds": newsfeeds, 
            "page_type": "Dashboard", "page_value": "Overview",
            "navIndicator": 'dashboard' }, context_instance=RequestContext(request))
