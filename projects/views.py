from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import *
from projects.forms import *
from issues.models import *

def home(request):

    projects = Project.objects.filter(product_owner=request.user)
    print projects
    return render_to_response("projects/projects.html", {'projects':projects}, context_instance=RequestContext(request))

def project_form(request):
    if request.method == 'POST':
        project = Project()
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():

            try:
                project = form.save()
            except:
                print 'unable to save project'

            if project.id:
                return redirect('projects.views.project_overview', project.id, permanent=True)
            else:
                return render_to_response("projects/project_form.html", {'form':form}, context_instance=RequestContext(request))
    else:
        form = ProjectForm()

    return render_to_response("projects/project_form.html", {'form':form}, context_instance=RequestContext(request))

def project_overview(request, project_id):

    try:
        project = Project.objects.get(pk=project_id)
        issues = Issue.objects.filter(project=project).order_by('-created')
    except:
        print 'project not found'
    return render_to_response("projects/project_overview.html", {'project_O':project, "issues":issues}, context_instance=RequestContext(request))
