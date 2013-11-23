# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'NewsFeedItem.comment'
        db.alter_column(u'newsfeed_newsfeeditem', 'comment', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'NewsFeedItem.description'
        db.alter_column(u'newsfeed_newsfeeditem', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'NewsFeedItem.new_value'
        db.alter_column(u'newsfeed_newsfeeditem', 'new_value', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'NewsFeedItem.old_value'
        db.alter_column(u'newsfeed_newsfeeditem', 'old_value', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'NewsFeedItem.comment'
        db.alter_column(u'newsfeed_newsfeeditem', 'comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'NewsFeedItem.description'
        db.alter_column(u'newsfeed_newsfeeditem', 'description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'NewsFeedItem.new_value'
        db.alter_column(u'newsfeed_newsfeeditem', 'new_value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'NewsFeedItem.old_value'
        db.alter_column(u'newsfeed_newsfeeditem', 'old_value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

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
        u'checklists.checklist': {
            'Meta': {'object_name': 'Checklist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'daily_reports.userdailyreport': {
            'Meta': {'object_name': 'UserDailyReport'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'food.foodrequest': {
            'Meta': {'object_name': 'FoodRequest'},
            'cost_per_quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'desired_completion': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'quantity_type': ('django.db.models.fields.CharField', [], {'default': '(1, 1)', 'max_length': '3'}),
            'request_completed_bool': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'request_completed_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'request_initiated': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'issues.issue': {
            'Meta': {'object_name': 'Issue'},
            'actual_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'actual_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assigned_to'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'browser_version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'criticality': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fixability': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'link_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'meta_issues': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.MetaIssue']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'point_of_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poc'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'projected_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'projected_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'r_and_d': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'screen_shot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'default': "'No Summary'", 'max_length': '140'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'uri_to_test': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'view_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wireframe': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'issues.metaissue': {
            'Meta': {'object_name': 'MetaIssue'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mi_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_story': ('django.db.models.fields.TextField', [], {})
        },
        u'newsfeed.newsfeeditem': {
            'Meta': {'object_name': 'NewsFeedItem'},
            'checklist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checklists.Checklist']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'daily_report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['daily_reports.UserDailyReport']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_change': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'food': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['food.FoodRequest']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Issue']", 'null': 'True', 'blank': 'True'}),
            'new_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'newsfeed_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'old_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']", 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        }
    }

    complete_apps = ['newsfeed']