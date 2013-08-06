from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from projects.models import *
from issues.models import Issue

import json

@login_required
def test(request):
    return render_to_response("charts/index.html", {}, context_instance=RequestContext(request))


@login_required
def home(request):
    users_dict = {}
    try:
        users = User.objects.all()
        for user in users:
            users_dict[user.id] = user.username
    except:
        print "Can't get users"

    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        issues = Issue.objects.all().order_by('project','-created')
        to_json_issues = []
        for issue in issues:
            json_issue = model_to_dict(issue)
            json_issue['created'] = issue.created
            json_issue['project_name'] = issue.project.name
            if issue.assigned_to:
                try:
                    json_issue['assigned_to'] = users_dict[issue.assigned_to.id]
                except Exception, e:
                    print e
            for k,v in json_issue.items():
                json_issue[k] = str(v)
            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Issues'
        to_json_issues = []

    return render_to_response("charts/charts.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


@login_required
def users_chart(request):
    users_dict = {}
    project_dict = {}
    try:
        users = User.objects.all()
        for user in users:
            users_dict[user.id] = user.username
    except:
        print "Can't get users"

    try:
        projects = Project.objects.all()
        for project in projects:
            project_dict[project.id] = project.name
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        issues = Issue.objects.all().order_by('-assigned_to', 'project')
        to_json_issues = []
        for issue in issues:
            json_issue = model_to_dict(issue)
            json_issue['created'] = issue.created
            json_issue['project_name'] = issue.project.name
            if issue.assigned_to:
                try:
                    json_issue['assigned_to'] = users_dict[issue.assigned_to.id]
                except Exception, e:
                    print e   
            for k,v in json_issue.items():
                json_issue[k] = str(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Issues'
        to_json_issues = []

    return render_to_response("charts/users_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


@login_required
def projects_chart(request):
    try:
        users = User.objects.all()
    except:
        print "Can't get users"

    try:
        to_json_projects = []
        projects = Project.objects.all().order_by('-created')
        for project in projects:
            json_project = model_to_dict(project)
            json_project['created'] = project.created
            for k,v in json_project.items():
                json_project[k] = str(v)
            to_json_projects.append(json_project)
    except:
        print 'Unable to grab all projects'
        projects = []

    issues = []

    return render_to_response("charts/projects_gantt_chart.html", {"projects": projects, "projects_dict": json.dumps(to_json_projects), "issues": json.dumps(issues), "users": users}, context_instance=RequestContext(request))


@login_required
def unassigned_issues_chart(request):
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        users = User.objects.all()
    except:
        print "Can't get users"

    try:
        issues = Issue.objects.filter(assigned_to=None).order_by('project', '-created')
        to_json_issues = []
        for issue in issues:
            json_issue = model_to_dict(issue)
            json_issue['created'] = issue.created
            json_issue['project_name'] = issue.project.name
            for k,v in json_issue.items():
                json_issue[k] = str(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Isssues'
        to_json_issues = []

    return render_to_response("charts/unassigned_issues_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


@login_required
def issues_by_user_chart(request, user_id):
    print 'user id is %s' % user_id
    try:
        users = User.objects.all()
    except:
        print "Can't get users"

    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        user = User.objects.get(pk=user_id)
        try:
            issues = Issue.objects.filter(assigned_to=user).order_by('project', '-created')
            to_json_issues = []
            for issue in issues:
                json_issue = model_to_dict(issue)
                json_issue['created'] = issue.created
                json_issue['project_name'] = issue.project.name
                for k,v in json_issue.items():
                    json_issue[k] = str(v)

                to_json_issues.append(json_issue)
        except Exception, e:
            print e
            print 'Unable to grab all Isssues'
            to_json_issues = []
    except:
        print "User doesn't exist!"
    return render_to_response("charts/issues_by_user_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


@login_required
def issues_by_project_chart(request, project_id):
    users_dict = {}
    try:
        users = User.objects.all()
        for user in users:
            users_dict[user.id] = user.username
    except:
        print "Can't get users"

    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        project = Project.objects.get(pk=project_id)
        try:
            issues = Issue.objects.filter(project=project).order_by('project', '-created')
            to_json_issues = []
            for issue in issues:
                json_issue = model_to_dict(issue)
                json_issue['created'] = issue.created
                if issue.assigned_to:
                    try:
                        json_issue['assigned_to'] = users_dict[issue.assigned_to.id]
                    except:
                        json_issue['assigned_to'] = None

                for k,v in json_issue.items():
                    json_issue[k] = str(v)

                to_json_issues.append(json_issue)
        except Exception, e:
            print e
            print 'Unable to grab all Isssues'
            to_json_issues = []
    except:
        print 'Unable to find project'
    return render_to_response("charts/issues_by_project_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))

@login_required
def meta_issues_by_project(request, project_id):
    pass
    '''
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        project = Project.objects.get(pk=project_id)
        try:
            meta_issues = MetaIssue.objects.filter(project=project)
            to_json_meta_issues = []
            for meta_issue in meta_issues:
                json_meta_issue = model_to_dict(meta_issue)
                json_meta_issue['created'] = meta_issue.created
                for k,v in json_meta_issue.items():
                    json_meta_issue[k] = str(v)

                to_json_meta_issues.append(json_meta_issue)
        except Exception, e:
            print e
            print 'Unable to grab all Isssues'
            to_json_meta_issues = []
    except:
        print 'Unable to find project'
    return render_to_response("charts/charts.html", {"projects": projects, "issues": json.dumps(to_json_meta_issues).replace("'", r"\'")}, context_instance=RequestContext(request))
    '''
