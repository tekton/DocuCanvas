from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from projects.models import *
from checklists.models import *
from checklists.forms import *


def edit(request, checklist_id):
    if request.method == 'POST':
        checklist = Checklist.objects.get(pk=checklist_id)
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            try:
                checklist = form.save()
            except Exception, e:
                print e
                print form.errors
            if checklist.id:
                return redirect('checklists.views.checklist_edit', checklist.id, permanent=True)
            else:
                return render_to_response('checklists/checklist_edit.html', {'form': form, "checklist": checklist}, context_instance=RequestContext(request))

    else:
        checklist = Checklist.objects.get(pk=checklist_id)
        form = ChecklistForm(instance=checklist, initial={"project": checklist.project}, auto_id=False)
    return render_to_response("checklists/checklist_edit.html", {"form": form, "checklist": checklist, "page_type": "Edit", "page_value": checklist.title}, context_instance=RequestContext(request))


def checklist_form(request):
    pass
    #return render_to_response("checklists/checklist_edit.html", {"checklist": checklist, "projects": projects, "page_type": "Project", "page_value": "Checklist"}, context_instance=RequestContext(request))


def checklist_form_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        projects = Project.objects.all()
        #checklist_form = ChecklistForm(initial={"project": project}, auto_id=False)
        form = ChecklistInstanceForm(initial={"checklist": checklist}, auto_id=False)
    except:
        print "Unable to find associated project"
        form = ChecklistInstanceForm()
    return render_to_response("checklists/checklist_form.html", {'form': form, "projects": projects, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def checklist_overview(request):
    pass
