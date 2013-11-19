# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaxYearForms'
        db.create_table(u'taxes_taxyearforms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tax_year_end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'taxes', ['TaxYearForms'])

        # Adding field 'InformationChecklist.tax_year'
        db.add_column(u'taxes_informationchecklist', 'tax_year',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['taxes.TaxYearForms'], unique=True),
                      keep_default=False)

        # Deleting field 'SupplyAnalysis.tax_year_end'
        db.delete_column(u'taxes_supplyanalysis', 'tax_year_end')

        # Adding field 'SupplyAnalysis.tax_year'
        db.add_column(u'taxes_supplyanalysis', 'tax_year',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['taxes.TaxYearForms']),
                      keep_default=False)

        # Deleting field 'ProjectAnalysis.tax_year_end'
        db.delete_column(u'taxes_projectanalysis', 'tax_year_end')

        # Adding field 'ProjectAnalysis.tax_year'
        db.add_column(u'taxes_projectanalysis', 'tax_year',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['taxes.TaxYearForms']),
                      keep_default=False)

        # Deleting field 'ContractAnalysis.tax_year_end'
        db.delete_column(u'taxes_contractanalysis', 'tax_year_end')

        # Adding field 'ContractAnalysis.tax_year'
        db.add_column(u'taxes_contractanalysis', 'tax_year',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['taxes.TaxYearForms']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'TaxYearForms'
        db.delete_table(u'taxes_taxyearforms')

        # Deleting field 'InformationChecklist.tax_year'
        db.delete_column(u'taxes_informationchecklist', 'tax_year_id')

        # Adding field 'SupplyAnalysis.tax_year_end'
        db.add_column(u'taxes_supplyanalysis', 'tax_year_end',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SupplyAnalysis.tax_year'
        db.delete_column(u'taxes_supplyanalysis', 'tax_year_id')

        # Adding field 'ProjectAnalysis.tax_year_end'
        db.add_column(u'taxes_projectanalysis', 'tax_year_end',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ProjectAnalysis.tax_year'
        db.delete_column(u'taxes_projectanalysis', 'tax_year_id')

        # Adding field 'ContractAnalysis.tax_year_end'
        db.add_column(u'taxes_contractanalysis', 'tax_year_end',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'ContractAnalysis.tax_year'
        db.delete_column(u'taxes_contractanalysis', 'tax_year_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'assumptions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'business_case': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'current_phase': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'deployment_server': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'deployment_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_requests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lead_developer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lead_developer'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phase_planning_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phase_planning_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phase_research_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phase_research_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'potential_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product_owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'product_owner'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'project_manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_manager'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'repository_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'taxes.contractanalysis': {
            'Meta': {'object_name': 'ContractAnalysis'},
            'company_name': ('django.db.models.fields.CharField', [], {'default': "'Channel Factory'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.TaxYearForms']"})
        },
        u'taxes.contractresearchcostanalysis': {
            'Meta': {'object_name': 'ContractResearchCostAnalysis'},
            'contractor_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.ContractAnalysis']"})
        },
        u'taxes.informationchecklist': {
            'Meta': {'object_name': 'InformationChecklist'},
            'acquisitions_dispositions_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'aquisitions_dispositions'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'acquisitions_dispositions_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'activity_time_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activity_time'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'activity_time_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'contract_research_analysis_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contract_research_analysis'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'contract_research_analysis_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'employee_wage_ammounts_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employee_wage_ammounts'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'employee_wage_ammounts_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'exact_filing_dates_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exact_filing_dates'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'exact_filing_dates_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'job_description'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'job_description_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'other_owned_companies_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'other_owned_companies'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'other_owned_companies_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'previous_credits_taken_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'previous_credits_taken'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'previous_credits_taken_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'project_listing_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_listing'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'project_listing_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'recent_company_chart_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recent_company_chart'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'recent_company_chart_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'supply_cost_analysis_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supply_cost_analysis'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'supply_cost_analysis_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tax_return_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tax_return'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'tax_return_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tax_return_prior_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tax_return_prior'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'tax_return_prior_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'tax_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.TaxYearForms']", 'unique': 'True'}),
            'trial_balance_1_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trial_balance_1'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'trial_balance_1_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'trial_balance_2_assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trial_balance_2'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'trial_balance_2_boolean': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        u'taxes.projectanalysis': {
            'Meta': {'object_name': 'ProjectAnalysis'},
            'client': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.TaxYearForms']"})
        },
        u'taxes.projectlistanalysis': {
            'Meta': {'object_name': 'ProjectListAnalysis'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.ProjectAnalysis']"})
        },
        u'taxes.supplyanalysis': {
            'Meta': {'object_name': 'SupplyAnalysis'},
            'company_name': ('django.db.models.fields.CharField', [], {'default': "'Channel Factory'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax_year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.TaxYearForms']"})
        },
        u'taxes.supplycostanalysis': {
            'Meta': {'object_name': 'SupplyCostAnalysis'},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['taxes.SupplyAnalysis']"}),
            'supplier_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'taxes.taxyearforms': {
            'Meta': {'object_name': 'TaxYearForms'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tax_year_end': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['taxes']