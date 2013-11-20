from django import forms

from taxes.models import InformationChecklist, ProjectAnalysis, ProjectListAnalysis, SupplyAnalysis, SupplyCostAnalysis, ContractAnalysis, ContractResearchCostAnalysis, TaxYearForms

class ProjectAnalysisForm(forms.ModelForm):
	class Meta:
		model = ProjectAnalysis


class ProjectListAnalysisForm(forms.ModelForm):
	class Meta:
		model = ProjectListAnalysis


class SupplyAnalysisForm(forms.ModelForm):
	class Meta:
		model = SupplyAnalysis


class SupplyCostAnalysisForm(forms.ModelForm):
	class Meta:
		model = SupplyCostAnalysis


class ContractAnalysisForm(forms.ModelForm):
	class Meta:
		model = ContractAnalysis


class ContractResearchCostAnalysisForm(forms.ModelForm):
	class Meta:
		model = ContractResearchCostAnalysis


class InformationChecklistForm(forms.ModelForm):
	class Meta:
		model = InformationChecklist


class TaxForm(forms.ModelForm):
	class Meta:
		model = TaxYearForms