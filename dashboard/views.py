from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projects.models import *
from projects.forms import *
from newsfeed.models import NewsFeedItem
from notifications.models import Notification, NotificationRecipient
from issues.models import *

@login_required
def home(request):
    '''
        need comments
    '''
    #issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
    try:
        issues = Issue.objects.filter(Q(assigned_to=request.user) & (Q(status="active") | Q(status="retest") | Q(status="unverified") | Q(status__isnull=True))).order_by('-created')
    except Exception, e:
        print e
    #pins = PinIssue.objects.select_related().filter(user=request.user)
    try:
        pins = Issue.objects.filter(pinissue__user=request.user).order_by('-created')
    except Exception, e:
        print e
    try:
        subscribed = Issue.objects.filter(subscriptiontoissue__user=request.user).order_by('-created')
    except Exception, e:
        print e

    try:
        newsfeeds = NewsFeedItem.objects.all().order_by('-id')[:20]
    except Exception, e:
        print e
    #projects = Project.objects.filter(lead_developer=request.user).order_by('-created')
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    try:
        notification_recipients = NotificationRecipient.objects.select_related('notification').filter(user=request.user, read=False)
        num_notifications = 0
        for notification in notification_recipients:
            num_notifications += 1
    except Exception, e:
        print e
        notifications = None
    #subscribed = SubscriptionToIssue.objects.select_related().filter(user=request.user)
    return render_to_response("theme/dashboard.html", {"issues": issues, "subscribed": subscribed,
            "projects": projects, "pins": pins, "newsfeeds": newsfeeds, "notifications": notification_recipients,
            "num_notifications": num_notifications, "page_type": "Dashboard", "page_value": "Overview",
            "navIndicator": 'dashboard'}, context_instance=RequestContext(request))
