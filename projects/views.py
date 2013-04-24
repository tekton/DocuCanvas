from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
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
