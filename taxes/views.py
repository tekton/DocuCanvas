from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from projects.models import Project
from taxes.models import InformationRequestChecklist, ProjectAnalysis, ProjectListAnalysis, SupplyAnalysis, SupplyCostAnalysis, ContractAnalysis, ContractResearchCostAnalysis
from taxes.forms import ProjectAnalysisForm, ProjectListAnalysisForm, SupplyAnalysisForm, SupplyCostAnalysisForm, ContractAnalysisForm, ContractResearchCostAnalysisForm
from datetime import date, timedelta

# Create your views here.
def createBaseForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

    project_analysis = ProjectAnalysis()
    project_item_formset = inlineformset_factory(ProjectAnalysis, ProjectListAnalysis, can_delete=False, extra=1)
    supply_analysis = SupplyAnalysis()
    supply_item_formset = inlineformset_factory(SupplyAnalysis, SupplyCostAnalysis, can_delete=False, extra=1)
    contract_analysis = ContractAnalysis()
    contract_item_formset = inlineformset_factory(ContractAnalysis, ContractResearchCostAnalysis, can_delete=False, extra=1)

    if request.method == 'POST':
        print request.POST
    else:
        project_formset = project_item_formset(instance=project_analysis)
        supply_formset = supply_item_formset(instance=supply_analysis)
        contract_formset = contract_item_formset(instance=contract_analysis)

    project_form = ProjectAnalysisForm(instance=project_analysis)
    supply_form = SupplyAnalysisForm(instance=supply_analysis)
    contract_form = ContractResearchCostAnalysisForm(instance=contract_analysis)

    return render_to_response("taxes/tax_form.html", {'projects': projects,
                                                      'project_analysis': project_analysis,
                                                      'supply_analysis': supply_analysis,
                                                      'contract_analysis': contract_analysis,
                                                      'project_formset': project_formset,
                                                      'supply_formset': supply_formset,
                                                      'contract_formset': contract_formset}, context_instance=RequestContext(request))


def submitProjectForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e

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
                                                      'project_form': project_form,
                                                      'project_analysis': project_analysis,
                                                      'project_formset': project_formset,}, context_instance=RequestContext(request))


def submitSupplyForm(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print e
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
                                                            'supply_formset': supply_formset}, context_instance=RequestContext(request))


def submitContractForm(request):
    try:
        projects = Project.objects.all()
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
                                                               'contract_formset': contract_formset}, context_instance=RequestContext(request))