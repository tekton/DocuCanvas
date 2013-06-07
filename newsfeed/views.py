# Create your views here.
from django.shortcuts import render_to_response, redirect
from issues.forms import IssueForm, IssueFullForm, CommentForm
from issues.models import Issue, IssueComment, IssueStatusUpdate
from projects.models import Project
from newsfeed.models import NewsFeedItem
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext

import json


@login_required
def get_next_newsfeeds(request):
    to_json = {'success': True}
    results = []

    if request.method == 'POST':
        start = int(request.POST['num_newsfeeds_shown'])
        end = start + 10
        try:
            next_newsfeeds = NewsFeedItem.objects.all().order_by('-id')[start:end]
            for newsfeed in next_newsfeeds:
                results.append(model_to_dict(newsfeed))
        except Exception, e:
            print e

    to_json['results'] = results
    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def newsfeed_action(request, newsfeed_type):
    try:
        newsfeeds = NewsFeedItem.objects.filter(newsfeed_type=newsfeed_type)
    except Exception, e:
        print e

    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    return render_to_response("newsfeed/newsfeed_type_log.html", {"newsfeeds": newsfeeds, "projects": projects, "page_type": "Newsfeed Type", "page_value": newsfeed_type}, context_instance=RequestContext(request))
