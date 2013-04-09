from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from projects.models import *
from checklists.models import *
from checklists.forms import *


def checklist_form(request):
    pass
    #return render_to_response("checklists/checklist_edit.html", {"checklist": checklist, "projects": projects, "page_type": "Project", "page_value": "Checklist"}, context_instance=RequestContext(request))


def checklist_form_project(request, project_id):

    try:
        project = Project.objects.get(pk=project_id)

    except Exception, e:
        print e
        return render_to_response("checklists/checklist_form.html", {}, context_instance=RequestContext(request))

    ChecklistLayoutItemsFormset = inlineformset_factory(Checklist, CheckListLayoutItems, can_delete=False, extra=1)
    checklist = Checklist()

    if request.method == 'POST':
        if 'add_checklist_item' in request.POST:
            cp = request.POST.copy()
            cp['checklistlayoutitems_set-TOTAL_FORMS'] = int(cp['checklistlayoutitems_set-TOTAL_FORMS']) + 1
            formset = ChecklistLayoutItemsFormset(cp, instance=checklist)
        elif 'submit' in request.POST:
            checklist_form = ChecklistForm(request.POST, instance=checklist)
            formset = ChecklistLayoutItemsFormset(request.POST, request.FILES, instance=checklist)
            if checklist_form.is_valid() and formset.is_valid():
                c = checklist_form.save()
                formset.save()
                c.save()
                return redirect('dashboard.views.home', permanent=True)

    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist, initial={"project": project}, auto_id=False)
    print 'abt to make view'
    return render_to_response("checklists/checklist_form.html", {'formset': formset, "checklist_form": checklist_form, "project_id": project_id, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def checklist_overview(request):
    pass
