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
	q_issue = Issue.objects.filter(Q(summary__contains=search) | Q(description__contains=search))
	q_help = HelpRequest.objects.filter(Q(name__contains=search) | Q(question__contains=search))

	return render_to_response("search/search_results.html", {'issues': q_issue, 'help_requests': q_help, "projects": projects}, context_instance=RequestContext(request))
