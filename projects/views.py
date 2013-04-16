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


def project_overview(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        issues = Issue.objects.filter(project=project).order_by('-created')
    except:
        print 'project not found'

    try:
        projects = Project.objects.all().order_by('-created')
    except:
        print 'Unable to load projects'

    return render_to_response("projects/project_overview.html", {'project_O': project, "issues": issues, "projects": projects, "page_type": "Project", "page_value": project.name}, context_instance=RequestContext(request))


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
