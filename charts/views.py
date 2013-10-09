from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db.models import Q

from projects.models import *
from issues.models import Issue

from datetime import date

import json

@login_required
def test(request):
    return render_to_response("charts/index.html", {}, context_instance=RequestContext(request))


'''
    Gantt chart of issues separated by project
'''
@login_required
def home(request):
    users_dict = {}
    try:
        users = User.objects.filter(is_staff=True)
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

        issues = Issue.objects.all().order_by('project', 'assigned_to', '-created')
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
            for k, v in json_issue.items():
                json_issue[k] = unicode(v)
            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Issues'
        to_json_issues = []

    return render_to_response("charts/charts.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


'''
    Gantt chart of issues separated by user
'''
@login_required
def users_chart(request):
    users_dict = {}
    project_dict = {}
    try:
        users = User.objects.filter(is_staff=True)
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
        issues = Issue.objects.filter(Q(projected_start__isnull=False, projected_end__isnull=False) | (Q(actual_start__isnull=False, actual_end__isnull=False))).order_by('-assigned_to', 'project', '-created')
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
                json_issue[k] = unicode(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Issues'
        to_json_issues = []

    return render_to_response("charts/users_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


'''
    Gantt chart of all projects
'''
@login_required
def projects_chart(request):
    try:
        users = User.objects.filter(is_staff=True)
    except:
        print "Can't get users"

    try:
        to_json_projects = []
        projects = Project.objects.all().order_by('-created')
        for project in projects:
            json_project = model_to_dict(project)
            json_project['created'] = project.created
            for k,v in json_project.items():
                json_project[k] = unicode(v)
            to_json_projects.append(json_project)
    except:
        print 'Unable to grab all projects'
        projects = []

    issues = []

    return render_to_response("charts/projects_gantt_chart.html", {"projects": projects, "projects_dict": json.dumps(to_json_projects), "issues": json.dumps(issues), "users": users}, context_instance=RequestContext(request))


'''
    Gantt chart of issues that have not been assigned yet
'''
@login_required
def unassigned_issues_chart(request):
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        users = User.objects.filter(is_staff=True)
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
                json_issue[k] = unicode(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Isssues'
        to_json_issues = []

    return render_to_response("charts/unassigned_issues_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


'''
    Gantt chart of issues that do not have a projected start, projected end, actual start, or actual end
'''
@login_required
def unscheduled_issues_chart(request):
    users_dict = {}
    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        users = User.objects.filter(is_staff=True)
        for user in users:
            users_dict[user.id] = user.username
    except:
        print "Can't get users"

    try:
        issues = Issue.objects.filter(Q(projected_start__isnull=True, projected_end__isnull=True) | (Q(actual_start__isnull=True, actual_end__isnull=True))).order_by('project', '-created')
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
                json_issue[k] = unicode(v)

            to_json_issues.append(json_issue)
    except Exception, e:
        print e
        print 'Unable to grab all Isssues'
        to_json_issues = []

    return render_to_response("charts/unscheduled_issues_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users}, context_instance=RequestContext(request))


'''
    Gantt chart for all issues assigned to user with id "user_id"
'''
@login_required
def issues_by_user_chart(request, user_id):

    try:
        users = User.objects.filter(is_staff=True)
    except:
        print "Can't get users"
        users = []
        

    try:
        assigned_to = User.objects.get(pk=user_id)
    except:
        assigned_to = "User does not exist!"

    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'
        projects = []

    try:
        user = User.objects.get(pk=user_id)
        try:
            #issues = Issue.objects.filter(assigned_to=user ).order_by('project', '-created')
            issues = Issue.objects.filter((Q(assigned_to=user) & Q(projected_start__isnull=False, projected_end__isnull=False)) | (Q(assigned_to=user) & Q(actual_start__isnull=False, actual_end__isnull=False)) ).order_by('project', '-created')
            to_json_issues = []
            for issue in issues:
                json_issue = model_to_dict(issue)
                json_issue['created'] = issue.created
                json_issue['project_name'] = issue.project.name
                for k,v in json_issue.items():
                    json_issue[k] = unicode(v)

                to_json_issues.append(json_issue)
        except Exception, e:
            print e
            print 'Unable to grab all Isssues'
            to_json_issues = []
    except:
        print "User doesn't exist!"

    return render_to_response("charts/issues_by_user_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users, "assigned_to": assigned_to}, context_instance=RequestContext(request))


'''
    Gantt chart for all issues associated with project with id "project_id"
'''
@login_required
def issues_by_project_chart(request, project_id):
    users_dict = {}
    try:
        users = User.objects.filter(is_staff=True)
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
                    json_issue[k] = unicode(v)

                to_json_issues.append(json_issue)
        except Exception, e:
            print e
            print 'Unable to grab all Isssues'
            to_json_issues = []
    except:
        print 'Unable to find project'
        project = Project()
    return render_to_response("charts/issues_by_project_gantt_chart.html", {"projects": projects, "issues": json.dumps(to_json_issues), "users": users, "project": project}, context_instance=RequestContext(request))


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


@login_required
def autoSchedule(request):
    projects = Project.objects.all()
    try:
        issues = Issue.objects.filter(assigned_to=request.user).exclude(status='fixed').exclude(status='not_a_bug').exclude(status='wont_fix').exclude(status='duplicate').order_by('created')
    except Exception as e:
        print e

    critical_to_json = []
    past_due_to_json = []
    due_soon_to_json = []
    regular_to_json = []

    # Sort assigned issues into appropriate subgroup... based on urgency of issue completion
    for issue in issues:
        # if/else protects later code in the instance that issue due date is not an active field
        try:
            if issue.due_date:
                total_time = (date.today() - issue.due_date).total_seconds()
            else:
                total_time = 432000
            if issue.criticality:
                criticality = issue.criticality
            else:
                criticality = 0

            json_issue = model_to_dict(issue)
            json_issue['created'] = issue.created

            # Adding various
            if issue.actual_start:
                json_issue['actual_start'] = issue.actual_start
            if issue.projected_end:
                json_issue['projected_end'] = issue.projected_end
            if issue.actual_end:
                json_issue['actual_end'] = issue.actual_end

            for k,v in json_issue.items():
                json_issue[k] = unicode(v)

            if criticality > 7:
                critical_to_json.append(json_issue)
            elif total_time <= 0:
                past_due_to_json.append(json_issue)
            elif total_time < 432000:
                due_soon_to_json.append(json_issue)
            else:
                regular_to_json.append(json_issue)
        except Exception as e:
            print e
            print "Error adding issue '" + issue.summary + "' to auto scheduler"

    # Merging each list into a single list to pass to the front end.
    assigned_issues = []
    assigned_issues.extend(critical_to_json)
    assigned_issues.extend(past_due_to_json)
    assigned_issues.extend(due_soon_to_json)
    assigned_issues.extend(regular_to_json)

    return render_to_response('charts/auto_schedule.html', {'projects': projects, 
                                                        'issues': json.dumps(assigned_issues)}, context_instance=RequestContext(request))
    