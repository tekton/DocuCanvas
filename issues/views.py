# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import *
from issues.models import *
from issues.forms import *

def issue_form(request):
	if request.method == 'POST':
		issue = Issue()
		form = IssueForm(request.POST, instance=issue)
		if form.is_valid():
			try:
				issue = form.save()
			except:
				print "It ain't gonna work"	
			if issue.id:
				return redirect( 'issues.views.issue_overview', issue.id, permanent=True)
			else:
				return render_to_response('issues/issue_form.html', {'form':form}, context_instance=RequestContext(request))
	else:
		form = IssueForm()
		projects = Project()
		print form
	return render_to_response("issues/issue_form.html", {'form':form}, context_instance=RequestContext(request))

def issue_overview(request, issue_id):
	try:
		issue = Issue.objects.get(pk=issue_id)
	except:
		print "Somebody messed up the issue overview"
	return render_to_response("issues/issue_overview.html", {'issue_O':issue}, context_instance=RequestContext(request))