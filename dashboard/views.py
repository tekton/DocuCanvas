from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projects.models import *
from projects.forms import *
from issues.models import *


def home(request):
    #issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
    if request.user.is_authenticated():
        issues = Issue.objects.filter(assigned_to=request.user).order_by('-created')
        pins = PinIssue.objects.select_related().filter(user=request.user)
        #projects = Project.objects.filter(lead_developer=request.user).order_by('-created')
        projects = Project.objects.all().order_by('-created')
        subscribed = SubscriptionToIssue.objects.select_related().filter(user=request.user)
        return render_to_response("dashboard.html", {"issues": issues, "subscribed": subscribed, "projects": projects, "pins": pins, "page_type": "Dashboard", "page_value": "Overview"}, context_instance=RequestContext(request))
    else:
        return redirect('auth.views.login_func')
