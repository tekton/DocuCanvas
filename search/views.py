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


@login_required
def search(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    search = request.POST["searchText"]
    q_helpresponse = HelpResponse.objects.filter(Q(response__contains=search))
    json_response = {}
    response_count = 0
    for item in q_helpresponse:
        json_response["id-"+str(response_count)] = item.helprequest.id
        json_response["name-"+str(response_count)] = item.helprequest.name
        json_response["response-"+str(response_count)] = item.response
        response_count = response_count + 1
    q_issuecomment = IssueComment.objects.filter(Q(description__contains=search))
    json_comment = {}
    comment_count = 0
    for item in q_issuecomment:
        json_comment["id-"+str(comment_count)] = item.issue.id
        json_comment["summary-"+str(comment_count)] = item.issue.summary
        json_comment["comment-"+str(comment_count)] = item.description
        comment_count = comment_count + 1
    summary_count = 0
    q_issuesummary = Issue.objects.filter(Q(summary__contains=search))
    json_summary = {}
    for item in q_issuesummary:
        json_summary["id-"+str(summary_count)] = item.id
        json_summary["summary-"+str(summary_count)] = item.summary
        summary_count = summary_count + 1
    q_issuedescription = Issue.objects.filter(Q(description__contains=search))
    json_description = {}
    description_count = 0
    for item in q_issuedescription:
        json_description["id-"+str(description_count)] = item.id
        json_description["summary-"+str(description_count)] = item.summary
        json_description["description-"+str(description_count)] = item.description
        description_count = description_count + 1
    q_helpname = HelpRequest.objects.filter(Q(name__contains=search))
    json_name = {}
    name_count = 0
    for item in q_helpname:
        json_name["id-"+str(name_count)] = item.id
        json_name["name-"+str(name_count)] = item.name
        name_count = name_count + 1
    q_helpquestion = HelpRequest.objects.filter(Q(question__contains=search))
    json_question = {}
    question_count = 0
    for item in q_helpquestion:
        json_question["id-"+str(question_count)] = item.id
        json_question["name-"+str(question_count)] = item.name
        json_question["question-"+str(question_count)] = item.question
        question_count = question_count + 1
    print json_name
    return render_to_response("search/search_results.html", {"search": search, "projects": projects, "comment_count": comment_count, "issue_comment": json.dumps(json_comment), "summary_count": summary_count, "issue_summary": json.dumps(json_summary), "description_count": description_count, "issue_description": json.dumps(json_description), "response_count": response_count, "help_response": json.dumps(json_response), "name_count": name_count, "help_name": json.dumps(json_name), "question_count": question_count, "help_question": json.dumps(json_question)}, context_instance=RequestContext(request))


@login_required
def searchGlobal(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    search = request.POST["searchText"]
    
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
                                                             "search": search}, context_instance=RequestContext(request))
