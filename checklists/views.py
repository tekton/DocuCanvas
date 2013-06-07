import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from projects.models import *
from checklists.models import *
from checklists.forms import *


@login_required
def project_checklists(request, project_id):
    print 'in project checklists'
    try:
        projects = Project.objects.all()
        project = Project.objects.get(pk=project_id)
    except Exception, e:
        print e

    try:
        checklists = Checklist.objects.filter(project=project)
    except Exception, e:
        print e

    checklist_instances = {}
    for checklist in checklists:
        try:
            checklist_instance_list = ChecklistInstance.objects.filter(checklist=checklist).order_by('-created')
            for checklist_instance in checklist_instance_list:
                checklist_instance_key = checklist.name + str(checklist_instance.id)
                checklist_instances[checklist_instance_key] = checklist_instance
        except Exception, e:
            print e
            print 'Checklist Instance not found'

    return render_to_response("checklists/checklists.html", {"checklists": checklists, "checklist_instances": checklist_instances, "project": project, "projects": projects,  "project_id": project_id, "page_type": project.name, "page_value": "Checklists"}, context_instance=RequestContext(request))


@login_required
def checklist_edit(request, checklist_id):
    try:
        checklist = Checklist.objects.get(pk=checklist_id)
    except:
        print 'couldnt find checklist'
        formset = ChecklistForm()
        checklist = Checklist()

    try:
        num_checklist_layout_items = CheckListLayoutItems.objects.filter(Checklist=checklist).count()
    except Exception, e:
        print e
        print 'couldnt count number of checklistlayoutitems'

    ChecklistLayoutItemsFormset = inlineformset_factory(Checklist, CheckListLayoutItems, can_delete=False, extra=0)


    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST, instance=checklist)
        formset = ChecklistLayoutItemsFormset(request.POST, instance=checklist)

        if checklist_form.is_valid() and formset.is_valid():
            print 'success'
            checklist_form.save()
            formset.save()
        else:
            print checklist_form.errors
            print formset.errors
    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist)


    return render_to_response("checklists/checklist_overview.html", {"formset": formset, "checklist_form": checklist_form, "checklist": checklist, "num_checklist_items": num_checklist_layout_items, "page_type": checklist.project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


@login_required
def instance_edit(request, checklist_instance_id):
    try:
        checklist_instance = ChecklistInstance.objects.get(pk=checklist_instance_id)
        # CHECK IF CHECKLIST LAYOUT ITEMS HAS BEEN UPDATED, IF SO UPDATE CHECKLIST INSTANCE TAGS
    except Exception, e:
        print e
        checklist_instance = ChecklistInstance()

    ChecklistTagsFormset = inlineformset_factory(ChecklistInstance, ChecklistTag, can_delete=False, extra=0)
    if request.method == 'POST':
        print 'hi'
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
            print completion_count
            print total_forms

            if completion_count == total_forms:
                checklist_instance.completion_status = True
                checklist_instance.save()

            checklist_instance_form.save()
            formset.save()
            return project_checklists(request, checklist_instance.checklist.project.id)
    else:
        formset = ChecklistTagsFormset(instance=checklist_instance)

    checklist_instance_form = ChecklistInstanceFullForm(instance=checklist_instance)
    return render_to_response("checklists/checklist_edit.html", {"form": formset, "checklist_instance_form": checklist_instance_form, "checklist_instance": checklist_instance, "page_type": checklist_instance.title, "page_value": "Checklist"}, context_instance=RequestContext(request))


@login_required
def toggle_checkbox(request):
    to_json = {}

    try:
        checklist_tag = ChecklistTag.objects.get(pk=request.POST['checklist_tag_id'])
        if checklist_tag.completion_status is True:
            checklist_tag.completion_status = False
        else:
            checklist_tag.completion_status = True

        checklist_tag.save()
        to_json['status'] = "Completed Check"
    except Exception, e:
        to_json['status'] = e

    if request.POST['all_checked'] == "true":
        print 'all checked'
        try:
            checklist_instance = ChecklistInstance.objects.get(pk=checklist_tag.checklist_instance.id)
            checklist_instance.completion_status = True
            checklist_instance.save()
            to_json['status'] = "All Checkboxes Checked"
        except Exception, e:
            print e
    elif request.POST['all_checked'] == "false":
        checklist_instance = ChecklistInstance.objects.get(pk=checklist_tag.checklist_instance.id)
        checklist_instance.completion_status = False
        checklist_instance.save()

    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def submit_tag_comment(request):
    to_json = {}

    try:
        checklist_tag = ChecklistTag.objects.get(pk=request.POST['checklist_tag_id'])
        checklist_tag.comment = request.POST['comment']
        checklist_tag.save()
        to_json['status'] = "Saved Comment"
    except Exception, e:
        to_json['status'] = e
    return HttpResponse(json.dumps(to_json), mimetype='application/json')


@login_required
def new_instance(request, checklist_id):
    try:
        checklist = Checklist.objects.get(pk=checklist_id)
        checklist_layout_items = CheckListLayoutItems.objects.filter(Checklist=checklist).order_by('order')
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

    #return project_checklists(request, checklist.project.id)
    return redirect('checklists.views.project_checklists', checklist.project.id)


@login_required
def checklist_form_project(request, project_id):
    try:
        projects = Project.objects.all()
        project = Project.objects.get(pk=project_id)

    except Exception, e:
        print e
        return render_to_response("checklists/checklist_form.html", {}, context_instance=RequestContext(request))

    ChecklistLayoutItemsFormset = inlineformset_factory(Checklist, CheckListLayoutItems, can_delete=False, extra=1)
    checklist = Checklist()

    if request.method == 'POST':
        checklist_form = ChecklistForm(request.POST, instance=checklist)
        formset = ChecklistLayoutItemsFormset(request.POST, instance=checklist)
        if checklist_form.is_valid() and formset.is_valid():
            c = checklist_form.save()
            formset.save()
            print 'saving form'
            return redirect('checklists.views.project_checklists', c.project.id)
        else:
            print checklist_form.errors
            print formset.errors
    else:
        formset = ChecklistLayoutItemsFormset(instance=checklist)

    checklist_form = ChecklistForm(instance=checklist, initial={"project": project}, auto_id=False)
    return render_to_response("checklists/checklist_form.html", {'formset': formset, "checklist_form": checklist_form, "project": project, "projects": projects, "page_type": project.name, "page_value": "Checklist"}, context_instance=RequestContext(request))


@login_required
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
