from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.db.models import Q
from projects.models import *
from projects.forms import *
from issues.models import *

import json

@login_required
def home(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []
    #owned_projects = Project.objects.filter(product_owner=request.user)
    return render_to_response("projects/projects.html", {'projects': projects, "page_type": "Projects"}, context_instance=RequestContext(request))


@login_required
@permission_required("projects.make_project", raise_exception=True)
def project_form(request):
    if request.method == 'POST':
        project = Project()
        try:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():

                try:
                    project = form.save(request.user)
                except:
                    print 'unable to save project'
                if project.id:
                    return redirect('projects.views.project_overview', project.id)
                else:
                    return render_to_response("projects/project_form.html", {'form': form}, context_instance=RequestContext(request))
        except Exception, e:
            print "Error validating project fields"
            print e
    else:
        form = ProjectForm()

    try:
        projects = Project.objects.all()
    except:
        print 'Unable to grab all projects'

    return render_to_response("projects/project_wizard.html", {'form': form, "projects": projects, "page_type": "Project", "page_value": "New"}, context_instance=RequestContext(request))


@login_required
def project_overview(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        metas = MetaIssue.objects.filter(project=project)
        incomplete_issues = Issue.objects.filter(project=project).exclude(status='fixed').order_by('-created')
        fixed_issues = Issue.objects.filter(project=project, status='fixed').order_by('-created')
    except:
        print 'project not found'

    try:
        # NEED TO CHANGE TO FILTER PROJECTS VIEABLE BY USER
        projects = Project.objects.all().order_by('-created')
    except:
        print 'Unable to load projects'

    try:
        project_planner_items = ProjectPlannerItem.objects.filter(project=project)
    except:
        print 'Unable to load project planner items'
        project_planner_items = []

    try:
        connections = ProjectPlannerItemConnection.objects.select_related().filter(project=project)
        to_json_connections = []
        for connection in connections:
            to_append = model_to_dict(connection)
            to_append['source'] = connection.source.meta_issue.id
            to_append['target'] = connection.target.meta_issue.id
            to_json_connections.append(to_append)
    except:
        print 'Unable to load project planner item connections'
        connections = []

    return render_to_response("projects/project_overview.html", {'project': project, "project_planner_items": project_planner_items, "connections": json.dumps(to_json_connections), "metas": metas, "incomplete_issues": incomplete_issues, "fixed_issues":fixed_issues, "projects": projects, "page_value": project.name}, context_instance=RequestContext(request))


@login_required
def project_stats(request, project_id):
    projects = Project.objects.all()
    try:
        project = Project.objects.get(pk=project_id)

        issues = Issue.objects.filter(project=project)

        blank_issues = issues.filter(status=None)
        not_a_bug_issues = issues.filter(status='not_a_bug')
        wont_fix_issues = issues.filter(status='wont_fix')
        duplicate_issues = issues.filter(status='duplicate')
        active_issues = issues.filter(status='active')
        fixed_issues = issues.filter(status='fixed')
        retest_issues = issues.filter(status='retest')
        unverified_issues = issues.filter(status='unverified')

        blank_count = blank_issues.count()
        not_a_bug_count = not_a_bug_issues.count()
        wont_fix_count = wont_fix_issues.count()
        duplicate_count = duplicate_issues.count()
        active_count = active_issues.count()
        fixed_count = fixed_issues.count()
        retest_count = retest_issues.count()
        unverified_count = unverified_issues.count()

        criticality_issues = Issue.objects.filter(Q(project=project) & (Q(status='active') | Q(status='unverified') | Q(status='duplicate'))).order_by('-criticality')
        bugs_for_review = Issue.objects.filter(Q(project=project) & (Q(status='wont_fix') | Q(status='not_a_bug') | Q(status='retest') | Q(status='duplicate')))
    except Exception, e:
        print e

    return render_to_response("projects/project_stats.html", {"project": project, "projects": projects, "criticality_issues": criticality_issues, "bugs_for_review": bugs_for_review, "blank_issues": blank_issues, "not_a_bug_issues": not_a_bug_issues, "wont_fix_issues": wont_fix_issues, "duplicate_issues": duplicate_issues, "active_issues": active_issues, "fixed_issues": fixed_issues, "retest_issues": retest_issues, "unverified_issues": unverified_issues, "blank_count": blank_count, "not_a_bug_count": not_a_bug_count, "wont_fix_count": wont_fix_count, "duplicate_count": duplicate_count, "active_count": active_count, "fixed_count": fixed_count, "retest_count": retest_count, "unverified_count": unverified_count, "page_type": project.name, "page_value":"Report"}, context_instance=RequestContext(request))


@login_required
def save_project_planner_item(request):
    to_json = {'success': True}

    if request.method == 'POST':
        try:
            meta_issue = MetaIssue.objects.get(pk=request.POST['item_id'])

            try:
                project_planner_item = ProjectPlannerItem.objects.get(meta_issue=meta_issue)
                project_planner_item.x_coordinate = request.POST['x_coordinate']
                project_planner_item.y_coordinate = request.POST['y_coordinate']
                project_planner_item.save()
            except:
                try:
                    project = Project.objects.get(pk=request.POST['project_id'])
                    project_planner_item = ProjectPlannerItem()
                    project_planner_item.project = project
                    project_planner_item.meta_issue = meta_issue
                    project_planner_item.type = request.POST['type']
                    project_planner_item.x_coordinate = request.POST['x_coordinate']
                    project_planner_item.y_coordinate = request.POST['y_coordinate']
                    project_planner_item.save()
                except:
                    print 'Project does not exist'
                    to_json['success'] = False

        except Exception, e:
            print e
            print 'Meta Issue does not exist'
            to_json['success'] = False

    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def save_project_planner_item_connection(request):
    to_json = {'success': True}

    if request.method == 'POST':
        try:
            source_meta_issue = MetaIssue.objects.get(pk=request.POST['source_id'])
            target_meta_issue = MetaIssue.objects.get(pk=request.POST['target_id'])
            try:
                source = ProjectPlannerItem.objects.get(meta_issue=source_meta_issue)
                target = ProjectPlannerItem.objects.get(meta_issue=target_meta_issue)
                try:
                    project_planner_item_connection = ProjectPlannerItemConnection.objects.get(source=source, target=target)
                    to_json['response'] = 'Connection between ' + str(source.meta_issue.title) + ' and ' + str(target.meta_issue.title) + ' already exists!'
                except:
                    try:
                        project_planner_item_connection = ProjectPlannerItemConnection()
                        project_planner_item_connection.project = Project.objects.get(pk=request.POST['project_id'])
                        try:
                            project_planner_item_connection.source = source
                            project_planner_item_connection.target = target
                            project_planner_item_connection.save()
                        except Exception, e:
                            print 'Project Planner item does not exist'
                            print e
                            to_json['success'] = False
                    except Exception, e:
                        print e
                        print 'Project does not exist'
            except Exception, e:
                print e
                print 'Project Planner Item does not exist'
        except:
            print 'Meta Issue does not exist'
            print e
            to_json['success'] = False

    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def remove_project_planner_item_connection(request):
    pass


@login_required
@permission_required("projects.make_project", raise_exception=True)
def edit(request, project_id):
    projects = Project.objects.all()
    if request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            try:
                project = form.save(request.user)
            except Exception, e:
                print e
                print form.errors
            if project.id:
                return redirect('projects.views.project_overview', project.id)
            else:
                return render_to_response('projects/project_edit.html', {'form': form, "project": project}, context_instance=RequestContext(request))

    else:
        project = Project.objects.get(pk=project_id)
        form = ProjectForm(instance=project)
    return render_to_response("projects/project_edit.html", {"form": form, "project": project, "projects": projects, "page_type": "Project", "page_value": project.name}, context_instance=RequestContext(request))


def CodeNames(request):
    cn_projects = Project.objects.all()
    cn_meta = MetaIssue.objects.all()
    return render_to_response("projects/code_names.html", {"cn_projects": cn_projects, "cn_meta": cn_meta, "page_type": "Project", "page_value": "Code Names"}, context_instance=RequestContext(request))
