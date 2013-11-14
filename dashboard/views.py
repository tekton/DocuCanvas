from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import QueryDict
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
    try:
        users = User.objects.all()
    except Exception, e:
        print e
        users = []

    #issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
    try:
        issues = Issue.objects.filter(Q(assigned_to=request.user) & (Q(status="active") | Q(status="retest") | Q(status="unverified") | Q(status__isnull=True))).order_by('-created')
    except Exception, e:
        print e
        issues = []
    #pins = PinIssue.objects.select_related().filter(user=request.user)
    try:
        pins = Issue.objects.filter(pinissue__user=request.user).order_by('-created')
    except Exception, e:
        print e
        pins = []
    try:
        subscribed = Issue.objects.filter(subscriptiontoissue__user=request.user).order_by('-created')
    except Exception, e:
        print e
        subscribed = []

    try:
        newsfeeds = NewsFeedItem.objects.all().order_by('-id')[:20]
    except Exception, e:
        print e
        newsfeeds = []
    #projects = Project.objects.filter(lead_developer=request.user).order_by('-created')
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []

    try:
        notification_recipients = NotificationRecipient.objects.select_related('notification').filter(user=request.user, read=False)
        num_notifications = 0
        for notification in notification_recipients:
            num_notifications += 1
    except Exception, e:
        print e
        notification_recipients = None

    # print users
    #subscribed = SubscriptionToIssue.objects.select_related().filter(user=request.user)
    
    template = request.GET.get("template", "dashboard/dashboard.html")

    return render_to_response(template, {"issues": issues, "subscribed": subscribed,
            "projects": projects, "pins": pins, "newsfeeds": newsfeeds, "notifications": notification_recipients,
            "num_notifications": num_notifications, "users": users, "page_type": "Dashboard", "page_value": "Overview",
            "navIndicator": 'dashboard'}, context_instance=RequestContext(request))
