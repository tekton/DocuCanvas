# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from sprints.models import Sprint
from sprints.forms import SprintForm
from projects.models import Project
from issues.models import Issue

import datetime
import json


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


def autoCreateSprints(request):
	payload = {'success': True}
	today = datetime.datetime.today().weekday()
	date_format = "%Y.%m.%d"
	if today == 0:
		days_till_monday = 0
	else:
		days_till_monday = 7 - today
	count = 0
	start_date = datetime.datetime.today() + datetime.timedelta(days=days_till_monday)
	payload['message'] = []
	while(count < 5):
		try:
			sprint = Sprint()
			sprint.start = start_date
			sprint.end = start_date + datetime.timedelta(days=4)
			sprint.name = "Sprint " + sprint.start.strftime(date_format) + " - " + sprint.end.strftime(date_format)
		except Exception, e:
			payload['message'].append('failed to create %s' % sprint.name)
			payload['success'] = False
		try:
			check = Sprint.objects.filter(name=sprint.name)
			if check:
				count = count + 1
				payload['message'].append('%s already exists' % sprint.name)
				continue
		except:
			pass
		try:
			sprint.save()
			payload['message'].append('%s created successfully' % sprint.name)
		except Exception, e:
			payload['message'].append('failed to create %s' % sprint.name)
			payload['success'] = False
		start_date = start_date + datetime.timedelta(days=7)
		count = count + 1
	return HttpResponse(json.dumps(payload))
