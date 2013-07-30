from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.forms.models import model_to_dict

from projects.models import *
from issues.models import Issue

import json

@login_required
def test(request):
    return render_to_response("charts/test01.html", {}, context_instance=RequestContext(request))


@login_required
def home(request):
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        issues = Issue.objects.all()
        to_json_issues = []
        for issue in issues:

            json_issue = model_to_dict(issue)
            json_issue['created'] = issue.created
            for k,v in json_issue.items():
                issue_dict = {}
                json_issue[k] = str(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Isssues'
        to_json_issues

    return render_to_response("charts/charts.html", {"projects": projects, "issues": json.dumps(to_json_issues).replace("'", r"\'")}, context_instance=RequestContext(request))
