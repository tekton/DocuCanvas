# Create your views here.
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


@login_required
def search(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    search = request.POST['searchText']
    q_helpresponse = HelpResponse.objects.filter(Q(response__contains=search))
    q_issuecomment = IssueComment.objects.filter(Q(description__contains=search))
    q_issue = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
    q_help = HelpRequest.objects.filter(Q(name__contains=search) | Q(question__contains=search))
    issue = list(q_issue)
    response_to_issue = list()
    for comment in q_issuecomment:
        response_to_issue.append(comment.issue)
    issue += response_to_issue
    issue.sort()
    if issue:
        last_issue = issue[-1]
        for i in range(len(issue)-2, -1, -1):
            if last_issue == issue[i]:
                del help[i]
            else:
                last_issue = issue[i]
    help = list(q_help)
    response_to_help = list()
    for response in q_helpresponse:
        response_to_help.append(response.helprequest)
    help += response_to_help
    help.sort()
    if help:
        last_help = help[-1]
        for i in range(len(help)-2, -1, -1):
            if last_help == help[i]:
                del help[i]
            else:
                last_help = help[i]

    return render_to_response("search/search_results.html", {'issues': issue, 'help_requests': help, "projects": projects}, context_instance=RequestContext(request))
