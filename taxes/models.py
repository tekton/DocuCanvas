from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from projects.models import Project

# Create your models here.
class TaxYearForms(models.Model):
	tax_year_end = models.DateField()


class InformationChecklist(models.Model):
	tax_year = models.ForeignKey(TaxYearForms, unique=True)
	recent_company_chart_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='recent_company_chart')
	recent_company_chart_boolean = models.NullBooleanField(default=False)
	other_owned_companies_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='other_owned_companies')
	other_owned_companies_boolean = models.NullBooleanField(default=False)
	employee_wage_ammounts_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='employee_wage_ammounts')
	employee_wage_ammounts_boolean = models.NullBooleanField(default=False)
	supply_cost_analysis_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='supply_cost_analysis')
	supply_cost_analysis_boolean = models.NullBooleanField(default=False)
	contract_research_analysis_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='contract_research_analysis')
	contract_research_analysis_boolean = models.NullBooleanField(default=False)
	activity_time_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='activity_time')
	activity_time_boolean = models.NullBooleanField(default=False)
	project_listing_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='project_listing')
	project_listing_boolean = models.NullBooleanField(default=False)
	job_description_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='job_description')
	job_description_boolean = models.NullBooleanField(default=False)
	tax_return_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='tax_return')
	tax_return_boolean = models.NullBooleanField(default=False)
	tax_return_prior_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='tax_return_prior')
	tax_return_prior_boolean = models.NullBooleanField(default=False)
	acquisitions_dispositions_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='aquisitions_dispositions')
	acquisitions_dispositions_boolean = models.NullBooleanField(default=False)
	previous_credits_taken_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='previous_credits_taken')
	previous_credits_taken_boolean = models.NullBooleanField(default=False)
	trial_balance_1_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='trial_balance_1')
	trial_balance_1_boolean = models.NullBooleanField(default=False)
	trial_balance_2_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='trial_balance_2')
	trial_balance_2_boolean = models.NullBooleanField(default=False)
	exact_filing_dates_assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='exact_filing_dates')
	exact_filing_dates_boolean = models.NullBooleanField(default=False)


class ProjectAnalysis(models.Model):
	client = models.CharField(max_length=255)
	tax_year = models.ForeignKey(TaxYearForms)


class ProjectListAnalysis(models.Model):
	report = models.ForeignKey(ProjectAnalysis)
	contact = models.CharField(max_length=255)
	contact_number = models.CharField(max_length=255)
	project = models.ForeignKey(Project)


class SupplyAnalysis(models.Model):
	company_name = models.CharField(max_length=255, default='Channel Factory')
	tax_year = models.ForeignKey(TaxYearForms)


class SupplyCostAnalysis(models.Model):
	report = models.ForeignKey(SupplyAnalysis)
	supplier_name = models.CharField(max_length=255)
	account_id = models.CharField(max_length=255)
	cost = models.DecimalField(max_digits=20, decimal_places=2)


class ContractAnalysis(models.Model):
	company_name = models.CharField(max_length=255, default='Channel Factory')
	tax_year = models.ForeignKey(TaxYearForms)


class ContractResearchCostAnalysis(models.Model):
	report = models.ForeignKey(ContractAnalysis)
	contractor_name = models.CharField(max_length=255)
	project = models.ForeignKey(Project)
	cost = models.DecimalField(max_digits=20, decimal_places=2)

admin.site.register(ProjectAnalysis)
admin.site.register(ProjectListAnalysis)
admin.site.register(InformationChecklist)
admin.site.register(ContractAnalysis)