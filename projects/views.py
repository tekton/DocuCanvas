from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import *
from projects.forms import *
from issues.models import *


@login_required
def home(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
        projects = []
    #owned_projects = Project.objects.filter(product_owner=request.user)
    return render_to_response("theme/default/projects/projects.html", {'projects': projects, "page_type": "Projects"}, context_instance=RequestContext(request))


@login_required
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

    return render_to_response("theme/default/projects/project_wizard.html", {'form': form, "projects": projects, "page_type": "Project", "page_value": "New"}, context_instance=RequestContext(request))


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

    return render_to_response("theme/default/projects/project_overview.html", {'project_O': project, "metas": metas, "incomplete_issues": incomplete_issues, "fixed_issues":fixed_issues, "projects": projects, "page_type": "Project", "page_value": project.name}, context_instance=RequestContext(request))


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
