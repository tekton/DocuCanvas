# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User

from sprints.models import Sprint
from sprints.forms import SprintForm
from projects.models import Project
from issues.models import Issue
from daily_reports.models import ReportGroup, GroupMember

import datetime
import json


def createSprint(request):
	try:
		projects = Project.objects.all()
	except Exception as e:
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
		except Exception as e:
			print e
	form = SprintForm(instance=sprint)
	return render_to_response('sprints/create_sprint.html', {'sprint': sprint, 'form': form, 'projects': projects}, context_instance=RequestContext(request))


def viewSprint(request, sprint_id):
	try:
		projects = Project.objects.all()
	except Exception as e:
		print e
	try:
		sprint = Sprint.objects.get(pk=sprint_id)
	except Exception as e:
		print e
	try:
		issues = Issue.objects.filter(sprint=sprint)
	except Exception as e:
		print e
	return render_to_response('sprints/sprint_overview.html', {'sprint': sprint, 'issues': issues, 'projects': projects}, context_instance=RequestContext(request))


def viewAll(request):
	try:
		projects = Project.objects.all()
	except Exception as e:
		print e
	try:
		sprints = Sprint.objects.all()
	except Exception as e:
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
		except Exception as e:
			payload['message'].append('failed to create %s' % sprint.name)
			payload['success'] = False
		try:
			check = Sprint.objects.filter(name=sprint.name)
			if check:
				count = count + 1
				start_date = start_date + datetime.timedelta(days=7)
				payload['message'].append('%s already exists' % sprint.name)
				continue
		except:
			pass
		try:
			sprint.save()
			payload['message'].append('%s created successfully' % sprint.name)
		except Exception as e:
			payload['message'].append('failed to create %s' % sprint.name)
			payload['success'] = False
		start_date = start_date + datetime.timedelta(days=7)
		count = count + 1
	return HttpResponse(json.dumps(payload))


def selectGroup(request, sprint_id):
	try:
		projects = Project.objects.all()
	except Exception, e:
		print e
	try:
		sprint = Sprint.objects.get(pk=sprint_id)
	except Exception, e:
		print e
	try:
	    groups = ReportGroup.objects.all()
	except Exception, e:
		print e
	return render_to_response('sprints/select_group.html', {'projects': projects,
		                                                    'sprint': sprint,
		                                                    'groups': groups}, context_instance=RequestContext(request))


def assignSprint(request, sprint_id, group_id=0):
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
	if not group_id == 0:	
		try:
			group = ReportGroup.objects.get(pk=group_id)
		except Exception, e:
			print e
		try:
			users = GroupMember.objects.filter(group=group)
			user = []
			for thing in users:
				user.append(thing.user)
		except Exception, e:
			print e
			user = User.objects.all()
	else:
		try:
			user = User.objects.all()
		except Exception, e:
			raise e
	return render_to_response('sprints/sprints_assignable.html', {'sprint': sprint,
		                                                          'issues': issues,
		                                                          'projects': projects,
		                                                          'users': user,}, context_instance=RequestContext(request))