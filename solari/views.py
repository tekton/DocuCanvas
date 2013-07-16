from django.shortcuts import render_to_response, redirect
from issues.forms import IssueForm, IssueFullForm, CommentForm
from issues.models import Issue, IssueComment, IssueStatusUpdate
from projects.models import Project
from newsfeed.models import NewsFeedItem
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext

@login_required
def Main(request):
	newsfeeds = NewsFeedItem.objects.all().order_by('-id')[:50]
	projects = Project.objects.all()

	return render_to_response("solari/main.html", {
		"newsfeeds": newsfeeds,
		"projects": projects,
		}, context_instance=RequestContext(request))
