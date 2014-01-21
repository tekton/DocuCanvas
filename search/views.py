# Create your views here.
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.forms.models import model_to_dict
from accounts.forms import PermissionForm
from accounts.utils import get_permission_form_for_model, set_permissions_for_model

from projects.models import Project
from issues.models import Issue, IssueComment
from helpdesknew.models import HelpRequest, HelpResponse
from daily_reports.models import UserDailyReport, DailyReport

import celery


@login_required
def searchGlobal(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    message = None
    search = request.POST["searchText"]

    temp = search.lower()
    if temp[0:6] == 'issue:' and temp[6:].isdigit():
        try:
            issue = Issue.objects.get(pk=temp[6:])
            return redirect('issues.views.issue_overview', issue.id)
        except Exception, e:
            print e
    elif temp.isdigit():
        try:
            issue = Issue.objects.get(pk=temp)
            message = issue.id
        except Exception, e:
            print e

    
    q_issues = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
    q_helprequest = HelpRequest.objects.filter(Q(question__contains=search) | Q(name__contains=search))
    q_dailyreports = UserDailyReport.objects.filter(Q(description__contains=search))

    return render_to_response("search/search_results.html", {"issues": q_issues, 
                                                             "issue_count": q_issues.count(), 
                                                             "helps": q_helprequest, 
                                                             "help_count": q_helprequest.count(), 
                                                             "reports": q_dailyreports, 
                                                             "report_count": q_dailyreports.count(), 
                                                             "projects": projects, 
                                                             "search": search,
                                                             "message": message}, context_instance=RequestContext(request))
