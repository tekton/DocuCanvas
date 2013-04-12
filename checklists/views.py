from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from projects.models import *
from checklists.models import *
from checklists.forms import *


def edit(request, checklist_instance_id):

    checklist_instance = ChecklistInstance(pk=checklist_instance_id)

    ChecklistTagsFormset = inlineformset_factory(ChecklistInstance, ChecklistTag, can_delete=False, extra=0)
    if request.method == 'POST':
        checklist_instance_form = ChecklistInstanceFullForm(request.POST, instance=checklist_instance)
        formset = ChecklistTagsFormset(request.POST, instance=checklist_instance)
        if checklist_instance_form.is_valid() and formset.is_valid():
            checklist_instance_form.save()
            formset.save()

    return redirect('checklists.views.overview', checklist_instance_id, permanent=True)


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
            formset = ChecklistLayoutItemsFormset(request.POST, instance=checklist)
            if checklist_form.is_valid() and formset.is_valid():
                c = checklist_form.save()
                checklist_layout_items = formset.save()
                c.save()
                checklist_instance = ChecklistInstance()
                checklist_instance.checklist = c
                checklist_instance.title = c.name
                checklist_instance.save()
                for item in checklist_layout_items:
                    checklist_tag = ChecklistTag()
                    checklist_tag.checklist_instance = checklist_instance
                    checklist_tag.name = item.title
                    checklist_tag.save()

                return redirect('checklists.views.overview', checklist_instance.id, permanent=True)

    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist, initial={"project": project}, auto_id=False)
    return render_to_response("checklists/checklist_form.html", {'formset': formset, "checklist_form": checklist_form, "project_id": project_id, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def overview(request, checklist_id):
    try:
        checklist_instance = ChecklistInstance.objects.get(pk=checklist_id)
    except:
        print 'couldnt find checklist'
        formset = ChecklistInstanceForm()
        checklist_instance = ChecklistInstance()

    ChecklistTagsFormset = inlineformset_factory(ChecklistInstance, ChecklistTag, can_delete=False, extra=0)
    formset = ChecklistTagsFormset(instance=checklist_instance)
    checklist_instance_form = ChecklistInstanceForm(instance=checklist_instance, initial={"project": checklist_instance.checklist.project}, auto_id=False)
    return render_to_response("checklists/checklist_overview.html", {"formset": formset, "checklist_instance_form": checklist_instance_form, "checklist_instance_id": checklist_instance.id, "page_type": checklist_instance.checklist.project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))
