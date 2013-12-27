# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from sprints.models import Sprint
from sprints.forms import SprintForm
from projects.models import Project
from issues.models import Issue

import datetime


def createSprint(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	sprint = Sprint()
	if request.method == 'POST':
		print request.POST
		try:
			sprint.name = request.POST["name"]
			sprint.start = datetime.datetime.strptime(request.POST["start"], "%Y/%m/%d")
			sprint.end = datetime.datetime.strptime(request.POST["end"], "%Y/%m/%d")
			sprint.save()
			return redirect('sprints.views.viewSprint', sprint.id)
		except Exception, e:
			print e
	form = SprintForm(instance=sprint)
	return render_to_response('sprints/create_sprint.html', {'sprint': sprint, 'form': form, 'projects': projects}, context_instance=RequestContext(request))


def viewSprint(request, sprint_id):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		sprint = Sprint.objects.get(pk=sprint_id)
	except Exception, e:
		print e
	try:
		issues = Issue.objects.filter(sprint=sprint)
	except Exception, e:
		print e
	return render_to_response('sprints/sprint_overview.html', {'sprint': sprint, 'issues': issues, 'projects': projects}, context_instance=RequestContext(request))


def viewAll(request):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		sprints = Sprint.objects.all()
	except Exception, e:
		print e
	return render_to_response('sprints/all_sprints.html', {'sprints':sprints, 'projects': projects}, context_instance=RequestContext(request))
