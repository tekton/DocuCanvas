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
from accounts.views import cache_checkUserTemplate

import traceback

@login_required
def dashboard(request):
    '''
        need comments
    '''
    try:
        users = User.objects.all()
    except Exception, e:
        print(e)
        users = []

    #issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
    try:
        issues = Issue.objects.filter(Q(assigned_to=request.user) & (Q(status="active") | Q(status="retest") | Q(status="unverified") | Q(status__isnull=True))).order_by('-created')
    except Exception, e:
        print(e)
        issues = []
    #pins = PinIssue.objects.select_related().filter(user=request.user)
    try:
        pins = Issue.objects.filter(pinissue__user=request.user).order_by('-created')
    except Exception, e:
        print(e)
        pins = []
    try:
        subscribed = Issue.objects.filter(subscriptiontoissue__user=request.user).order_by('-created')
    except Exception, e:
        print(e)
        subscribed = []

    try:
        newsfeeds = NewsFeedItem.objects.all().order_by('-id')[:20]
    except Exception, e:
        print(e)
        newsfeeds = []
    #projects = Project.objects.filter(lead_developer=request.user).order_by('-created')
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
        projects = []

    try:
        notification_recipients = NotificationRecipient.objects.select_related('notification').filter(user=request.user, read=False)
        num_notifications = 0
        for notification in notification_recipients:
            num_notifications += 1
    except Exception, e:
        print(e)
        notification_recipients = None

    # get user setting for dashboard layout...
    dashboardLayout = "col0[0]=module-pinned&col0[1]=module-assigned&col1[0]=module-newsfeed"
    try:
        cache_check = cache_checkUserTemplate(request.user, "dashboardLayout")
        if cache_check:
            dashboardLayout = cache_check
    except Exception as e:
        print(e)
        dashboardLayout = "col0[0]=module-pinned&col0[1]=module-assigned&col1[0]=module-newsfeed"
    # print(users)
    #subscribed = SubscriptionToIssue.objects.select_related().filter(user=request.user)
    # attempt to get the user defined template first, then check for an override template
    stack = traceback.extract_stack()
    filename, codeline, viewName, text = stack[-1]
    default = "dashboard/dashboard.html"
    try:
        cache_template = cache_checkUserTemplate(request.user, viewName)
        if cache_template:
            default = cache_template
    except Exception as e:
        # only print(if debug is really necisary)
        print("Unable to get template from cache :: ".format(str(e)))
        pass
    template = request.GET.get("template", default)
    return render_to_response(template, {"issues": issues, 
                                         "subscribed": subscribed,
                                         "projects": projects,
                                         "pins": pins,
                                         "newsfeeds": newsfeeds,
                                         "notifications": notification_recipients,
                                         "num_notifications": num_notifications,
                                         "users": users,
                                         "page_type": "Dashboard",
                                         "page_value": "Overview",
                                         "navIndicator": 'dashboard',
                                         "dashboardLayout": dashboardLayout,},
                             context_instance=RequestContext(request))
