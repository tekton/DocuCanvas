from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from projects.models import *
from checklists.models import *
from checklists.forms import *


def project_checklists(request, project_id):
    print 'in project checklists'
    project = Project.objects.get(pk=project_id)
    checklists = Checklist.objects.filter(project=project)

    checklist_instances = {}
    for checklist in checklists:
        print checklist.name
        try:
            #checklist_instances[checklist.name] = ChecklistInstance.objects.get(checklist=checklist)
            checklist_instance_list = ChecklistInstance.objects.filter(checklist=checklist)
            for checklist_instance in checklist_instance_list:
                checklist_instance_key = checklist.name + str(checklist_instance.id)
                checklist_instances[checklist_instance_key] = checklist_instance
        except Exception, e:
            print e
            print 'Checklist Instance not found'

    return render_to_response("checklists/checklists.html", {"checklists": checklists, "checklist_instances": checklist_instances, "project_id": project_id, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def checklist_edit(request, checklist_id):
    try:
        checklist = Checklist.objects.get(pk=checklist_id)
    except:
        print 'couldnt find checklist'
        formset = ChecklistForm()
        checklist = Checklist()

    ChecklistLayoutItemsFormset = inlineformset_factory(Checklist, CheckListLayoutItems, can_delete=False, extra=0)

    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST, instance=checklist)
        formset = ChecklistLayoutItemsFormset(request.POST, instance=checklist)

        if checklist_form.is_valid() and formset.is_valid():
            checklist_form.save()
            formset.save()
    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist)
    return render_to_response("checklists/checklist_overview.html", {"formset": formset, "checklist_form": checklist_form, "checklist_id": checklist.id, "page_type": checklist.project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def instance_edit(request, checklist_instance_id):

    try:
        checklist_instance = ChecklistInstance.objects.get(pk=checklist_instance_id)
        # CHECK IF CHECKLIST LAYOUT ITEMS HAS BEEN UPDATED, IF SO UPDATE CHECKLIST INSTANCE TAGS
    except Exception, e:
        print e
        checklist_instance = ChecklistInstance()

    ChecklistTagsFormset = inlineformset_factory(ChecklistInstance, ChecklistTag, can_delete=False, extra=0)
    if request.method == 'POST':
        checklist_instance_form = ChecklistInstanceFullForm(request.POST, instance=checklist_instance)
        formset = ChecklistTagsFormset(request.POST, instance=checklist_instance)

        if checklist_instance_form.is_valid() and formset.is_valid():
            total_forms = int(request.POST['checklisttag_set-TOTAL_FORMS'])
            i = 0
            completion_count = 0
            while i < total_forms:
                completion_status_key = "checklisttag_set-" + str(i) + "-completion_status"
                try:
                    request.POST[completion_status_key]
                    completion_count += 1
                except Exception, e:
                    print e
                i += 1

            if completion_count == total_forms:
                checklist_instance.completion_status = True
                checklist_instance.save()

            checklist_instance_form.save()
            formset.save()
    else:
        formset = ChecklistTagsFormset(instance=checklist_instance)

    checklist_instance_form = ChecklistInstanceFullForm(instance=checklist_instance)
    return render_to_response("checklists/checklist_edit.html", {"form": formset, "checklist_instance_form": checklist_instance_form, "checklist_instance": checklist_instance, "page_type": checklist_instance.title, "page_value": "Edit"}, context_instance=RequestContext(request))


def new_instance(request, checklist_id):
    print 'in new instance'
    try:
        checklist = Checklist.objects.get(pk=checklist_id)
        checklist_layout_items = CheckListLayoutItems.objects.filter(Checklist=checklist)
        checklist_instance = ChecklistInstance()
        checklist_instance.checklist = checklist
        checklist_instance.title = checklist.name
        checklist_instance.save()
        for item in checklist_layout_items:
            checklist_tag = ChecklistTag()
            checklist_tag.checklist_instance = checklist_instance
            checklist_tag.name = item.title
            checklist_tag.save()

    except Exception, e:
        print e

    return redirect('checklists.views.project_checklists', checklist.project.id, permanent=True)


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
                formset.save()
                return redirect('checklists.views.project_checklists', c.project.id, permanent=True)

    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist, initial={"project": project}, auto_id=False)
    return render_to_response("checklists/checklist_form.html", {'formset': formset, "checklist_form": checklist_form, "project_id": project_id, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


def overview(request, checklist_id):
    print 'in overview'
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
