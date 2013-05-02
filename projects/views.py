from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import *
from projects.forms import *
from issues.models import *


@login_required
def home(request):
    projects = Project.objects.filter(product_owner=request.user)
    return render_to_response("projects/projects.html", {'projects': projects, "page_type": "Project"}, context_instance=RequestContext(request))


@login_required
def project_form(request):
    if request.method == 'POST':
        project = Project()
        try:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():

                try:
                    project = form.save()
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

    return render_to_response("projects/project_form.html", {'form': form, "projects": projects, "page_type": "Project", "page_value": "New"}, context_instance=RequestContext(request))


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

    return render_to_response("projects/project_overview.html", {'project_O': project, "metas": metas, "incomplete_issues": incomplete_issues, "fixed_issues":fixed_issues, "projects": projects, "page_type": "Project", "page_value": project.name}, context_instance=RequestContext(request))


@login_required
def project_stats(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)

        not_a_bug_count = Issue.objects.filter(project=project, status='not_a_bug').count()
        wont_fix_count = Issue.objects.filter(project=project, status='wont_fix').count()
        duplicate_count = Issue.objects.filter(project=project, status='duplicate').count()
        active_count = Issue.objects.filter(project=project, status='active').count()
        fixed_count = Issue.objects.filter(project=project, status='fixed').count()
        retest_count = Issue.objects.filter(project=project, status='retest').count()
        unverified_count = Issue.objects.filter(project=project, status='unverified').count()

        active_issues = Issue.objects.filter(Q(project=project) & (Q(status='active') | Q(status='unverified') | Q(status='duplicate')))
        criticality_issues = Issue.objects.filter(Q(project=project) & (Q(status='active') | Q(status='unverified') | Q(status='duplicate'))).order_by('-criticality')
        bugs_for_review = Issue.objects.filter(Q(project=project) & (Q(status='wont_fix') | Q(status='not_a_bug') | Q(status='retest')))
        fixed_issues = Issue.objects.filter(project=project, status='fixed')

    except Exception, e:
        print e

    return render_to_response("projects/project_stats.html", {"project": project, "fixed_issues": fixed_issues, "criticality_issues": criticality_issues, "bugs_for_review": bugs_for_review, "active_issues": active_issues, "not_a_bug_count": not_a_bug_count, "wont_fix_count": wont_fix_count, "duplicate_count": duplicate_count, "active_count": active_count, "fixed_count": fixed_count, "retest_count": retest_count, "unverified_count": unverified_count, "page_type": project.name, "page_value":"Report"}, context_instance=RequestContext(request))


@login_required
def edit(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(pk=project_id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            try:
                project = form.save()
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
    return render_to_response("projects/project_edit.html", {"form": form, "project": project, "page_type": "Project", "page_value": project.name}, context_instance=RequestContext(request))


def CodeNames(request):
    cn_projects = Project.objects.all()
    cn_meta = MetaIssue.objects.all()
    return render_to_response("projects/code_names.html", {"cn_projects": cn_projects, "cn_meta": cn_meta, "page_type": "Project", "page_value": "Code Names"}, context_instance=RequestContext(request))
