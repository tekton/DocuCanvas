from django.forms.models import inlineformset_factory, model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.models import User
from projects.models import Project
from taxes.models import InformationChecklist, ProjectAnalysis, ProjectListAnalysis, SupplyAnalysis, SupplyCostAnalysis, ContractAnalysis, ContractResearchCostAnalysis, TaxYearForms
from taxes.forms import ProjectAnalysisForm, ProjectListAnalysisForm, SupplyAnalysisForm, SupplyCostAnalysisForm, ContractAnalysisForm, ContractResearchCostAnalysisForm, InformationChecklistForm, TaxForm
from datetime import date, timedelta

import json

def viewAllForms(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        tax_years = TaxYearForms.objects.all()
    except Exception, e:
        print e
    count = 0
    json_files = []
    for year in tax_years:
        try:
            project_analysis = ProjectAnalysis.objects.filter(tax_year=year)
            temp_proj = []
            for project in project_analysis:
                temp = model_to_dict(project)
                for k, v in temp.items():
                    temp[k] = unicode(v)
                temp_proj.append(temp)
        except Exception, e:
            print e
        try:
            supply_analysis = SupplyAnalysis.objects.filter(tax_year=year)
            temp_supp = []
            for supply in supply_analysis:
                temp = model_to_dict(supply)
                for k, v in temp.items():
                    temp[k] = unicode(v)
                temp_supp.append(temp)
        except Exception, e:
            print e
        try:
            contract_analysis = ContractAnalysis.objects.filter(tax_year=year)
            temp_cont = []
            for contract in contract_analysis:
                temp = model_to_dict(contract)
                for k, v in temp.items():
                    temp[k] = unicode(v)
                temp_cont.append(temp)
        except Exception, e:
            print e
        try:
            info_checklist = InformationChecklist.objects.get(tax_year=year)
            temp_info = model_to_dict(info_checklist)
            for k, v in temp_info.items():
                temp_info[k] = unicode(v)
        except Exception, e:
            print e
        temp_year = model_to_dict(year)
        for k,v in temp_year.items():
            temp_year[k] = unicode(v)
        index = str(count)
        json_temp = {'hi':{'tax_year': temp_year, 'projects': temp_proj, 'contracts': temp_cont, 'supplies': temp_supp, 'info': temp_info}}
        json_files.append(json_temp)
        count += 1
    json_count = []
    my_count = {'count': count}
    json_count.append(my_count)
    print json_files
    print json_count
    return render_to_response('taxes/display_all_forms.html', {'projects': projects,
                                                               'tax_years': json.dumps(json_files),
                                                               'item_count': json.dumps(json_count)}, context_instance=RequestContext(request))


def createTaxForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    tax_year = TaxYearForms()
    if request.method == 'POST':
        tax_form = TaxForm(request.POST, instance=tax_year)
        if tax_form.is_valid():
            tax_year = tax_form.save()
            return redirect('taxes.views.viewAllForms')
        else:
            print tax_form.errors
    else:
        tax_form = TaxForm(instance=tax_year)

    return render_to_response('taxes/tax_form.html', {'projects': projects}, context_instance=RequestContext(request))


def submitProjectForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e

    project_analysis = ProjectAnalysis()
    project_item_formset = inlineformset_factory(ProjectAnalysis, ProjectListAnalysis, can_delete=False, extra=1)

    if request.method == 'POST':
        print request.POST
        project_form = ProjectAnalysisForm(request.POST, instance=project_analysis)
        project_formset = project_item_formset(request.POST, instance=project_analysis)
        if project_form.is_valid() and project_formset.is_valid():
            try:
                project_analysis = project_form.save()
                project_formset.save()
                print "data saved"
                return redirect('taxes.views.submitProjectForm')
            except Exception, e:
                print e
        else:
            print project_form.errors
            print project_formset.errors
    project_formset = project_item_formset(instance=project_analysis)

    project_form = ProjectAnalysisForm(instance=project_analysis)

    return render_to_response("taxes/project_tax_form.html", {'projects': projects,
                                                              'tax_forms': tax_forms,
                                                              'project_form': project_form,
                                                              'project_analysis': project_analysis,
                                                              'project_formset': project_formset,}, context_instance=RequestContext(request))


def submitSupplyForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e
    supply_analysis = SupplyAnalysis()
    supply_item_formset = inlineformset_factory(SupplyAnalysis, SupplyCostAnalysis, can_delete=False, extra=1)
    if request.method == 'POST':
        supply_form = SupplyAnalysisForm(request.POST, instance=supply_analysis)
        supply_formset = supply_item_formset(request.POST, instance=supply_analysis)
        if supply_form.is_valid() and supply_formset.is_valid():
            try:
                supply_analysis = supply_form.save()
                supply_formset.save()
                return redirect('taxes.views.submitSupplyForm')
            except Exception, e:
                raise e
        else:
            print supply_form.errors
            print supply_formset.errors
    supply_formset = supply_item_formset(instance=supply_analysis)
    supply_form = SupplyAnalysisForm(instance=supply_analysis)

    return render_to_response("taxes/supply_tax_form.html", {'projects': projects,
                                                             'supply_form': supply_form,
                                                             'supply_analysis': supply_analysis,
                                                             'supply_formset': supply_formset,
                                                             'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def submitContractForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e
    contract_analysis = ContractAnalysis()
    contract_item_formset = inlineformset_factory(ContractAnalysis, ContractResearchCostAnalysis, can_delete=False, extra=1)
    if request.method == 'POST':
        contract_form = ContractAnalysisForm(request.POST, instance=contract_analysis)
        contract_formset = contract_item_formset(request.POST, instance=contract_analysis)
        if contract_form.is_valid and contract_formset.is_valid():
            try:
                contract_analysis = contract_form.save()
                contract_formset.save()
                return redirect('taxes.views.submitContractForm')
            except Exception, e:
                raise e
        else:
            print contract_form.errors
            print contract_formset.errors
    contract_formset = contract_item_formset(instance=contract_analysis)
    contract_form = ContractAnalysisForm(instance=contract_analysis)
    return render_to_response("taxes/contract_tax_form.html", {'projects': projects,
                                                               'contract_form': contract_form,
                                                               'contract_analysis': contract_analysis,
                                                               'contract_formset': contract_formset,
                                                               'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def editProjectForm(request, project_analysis_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        project_analysis = ProjectAnalysis.objects.get(pk=project_analysis_id)
    except Exception, e:
        print e
    try:
        project_list = ProjectListAnalysis.objects.filter(report=project_analysis)
    except Exception, e:
        print e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e

    if request.method == 'POST':
        print request.POST
        project_item_formset = inlineformset_factory(ProjectAnalysis, ProjectListAnalysis, can_delete=False, extra=1)
        project_formset = project_item_formset(request.POST, instance=project_analysis)
        if request.POST.getlist('client')[0] != project_analysis.client:
            try:
                project_analysis.client = request.POST.getlist('client')[0]
                project_analysis.save()
            except Exception, e:
                raise e
        if project_formset.is_valid():
            try:
                project_formset.save()
                return redirect('taxes.views.editProjectForm', project_analysis.id)
            except Exception, e:
                raise e
        else:
            print project_formset.errors
    return render_to_response("taxes/project_form_edit.html", {'projects': projects,
                                                               'project_analysis': project_analysis,
                                                               'project_list': project_list,
                                                               'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def deleteProjectListInstance(request, project_list_id):
    try:
        project_list = ProjectListAnalysis.objects.get(pk=project_list_id)
        project_analysis = project_list.report
        project_list.delete()
    except Exception, e:
        print e
    return redirect('taxes.views.editProjectForm', project_analysis.id)


def editSupplyForm(request, supply_analysis_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    try:
        supply_analysis = SupplyAnalysis.objects.get(pk=supply_analysis_id)
    except Exception, e:
        raise e
    try:
        supply_list = SupplyCostAnalysis.objects.filter(report=supply_analysis)
    except Exception, e:
        raise e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e
    if request.method == 'POST':
        supply_item_formset = inlineformset_factory(SupplyAnalysis, SupplyCostAnalysis, can_delete=False, extra=1)
        supply_formset = supply_item_formset(request.POST, instance=supply_analysis)
        if supply_formset.is_valid():
            try:
                supply_formset.save()
                return redirect('taxes.views.editSupplyForm', supply_analysis.id)
            except Exception, e:
                raise e
        else:
            print supply_formset.errors
    return render_to_response('taxes/supply_form_edit.html', {'projects': projects,
                                                              'supply_analysis': supply_analysis,
                                                              'supply_list': supply_list,
                                                              'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def editContractForm(request, contract_analysis_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        raise e
    try:
        contract_analysis = ContractAnalysis.objects.get(pk=contract_analysis_id)
    except Exception, e:
        raise e
    try:
        contract_list = ContractResearchCostAnalysis.objects.filter(report=contract_analysis)
    except Exception, e:
        raise e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e
    if request.method == 'POST':
        contract_item_formset = inlineformset_factory(ContractAnalysis, ContractResearchCostAnalysis, can_delete=False, extra=1)
        contract_formset = contract_item_formset(request.POST, instance=contract_analysis)
        if contract_formset.is_valid():
            try:
                contract_formset.save()
                return redirect('taxes.views.editContractForm', contract_analysis.id)
            except Exception, e:
                raise e
        else:
            print contract_formset.errors
    return render_to_response('taxes/contract_form_edit.html', {'projects': projects,
                                                                'contract_analysis': contract_analysis,
                                                                'contract_list': contract_list,
                                                                'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def createChecklist(request, info_checklist_id=-1):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        users = User.objects.all()
    except Exception, e:
        raise e
    try:
        tax_forms = TaxYearForms.objects.all()
    except Exception, e:
        raise e
    if info_checklist_id != -1:
        try:
            editing = True
            info_checklist = InformationChecklist.objects.get(pk=info_checklist_id)
            if request.method == 'POST':
                info_checklist_form = InformationChecklistForm(request.POST, instance=info_checklist)
                if info_checklist_form.is_valid():
                    info_checklist = info_checklist_form.save()
                    return redirect('taxes.views.createChecklist', info_checklist.id)
                else:
                    print info_checklist_form.errors
            else:
                info_checklist_form = InformationChecklistForm(instance=info_checklist)
        except Exception, e:
            print e
            return redirect('taxes.views.createChecklist')
    else:
        editing = False
        info_checklist = InformationChecklist()
        if request.method == 'POST':
            info_checklist_form = InformationChecklistForm(request.POST, instance=info_checklist)
            if info_checklist_form.is_valid():
                info_checklist = info_checklist_form.save()
                return redirect('taxes.views.createChecklist', info_checklist.id)
            else:
                print info_checklist_form.errors
        else:
            info_checklist_form = InformationChecklistForm(instance=info_checklist)
    return render_to_response('taxes/information_checklist_form.html', {'projects': projects,
                                                                        'users': users,
                                                                        'editing': editing,
                                                                        'info_checklist_form': info_checklist_form,
                                                                        'info_checklist': info_checklist,
                                                                        'tax_forms': tax_forms,}, context_instance=RequestContext(request))


def viewInfoChecklist(request, info_checklist_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
    try:
        info_checklist = InformationChecklist.objects.get(pk=info_checklist_id)
    except Exception, e:
        raise e
    return render_to_response('taxes/view_info_checklist.html', {'projects': projects, 'info_checklist': info_checklist}, context_instance=RequestContext(request))