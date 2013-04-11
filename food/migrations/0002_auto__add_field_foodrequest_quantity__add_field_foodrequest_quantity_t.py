# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FoodRequest.quantity'
        db.add_column('food_foodrequest', 'quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'FoodRequest.quantity_type'
        db.add_column('food_foodrequest', 'quantity_type',
                      self.gf('django.db.models.fields.CharField')(default=(1, 1), max_length=3),
                      keep_default=False)

        # Adding field 'FoodRequest.request_initiated'
        db.add_column('food_foodrequest', 'request_initiated',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FoodRequest.desired_completion'
        db.add_column('food_foodrequest', 'desired_completion',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FoodRequest.request_completed_bool'
        db.add_column('food_foodrequest', 'request_completed_bool',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FoodRequest.request_completed_date'
        db.add_column('food_foodrequest', 'request_completed_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'FoodRequest.cost_per_quantity'
        db.add_column('food_foodrequest', 'cost_per_quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'FoodRequest.total_cost'
        db.add_column('food_foodrequest', 'total_cost',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FoodRequest.quantity'
        db.delete_column('food_foodrequest', 'quantity')

        # Deleting field 'FoodRequest.quantity_type'
        db.delete_column('food_foodrequest', 'quantity_type')

        # Deleting field 'FoodRequest.request_initiated'
        db.delete_column('food_foodrequest', 'request_initiated')

        # Deleting field 'FoodRequest.desired_completion'
        db.delete_column('food_foodrequest', 'desired_completion')

        # Deleting field 'FoodRequest.request_completed_bool'
        db.delete_column('food_foodrequest', 'request_completed_bool')

        # Deleting field 'FoodRequest.request_completed_date'
        db.delete_column('food_foodrequest', 'request_completed_date')

        # Deleting field 'FoodRequest.cost_per_quantity'
        db.delete_column('food_foodrequest', 'cost_per_quantity')

        # Deleting field 'FoodRequest.total_cost'
        db.delete_column('food_foodrequest', 'total_cost')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'food.foodrequest': {
            'Meta': {'object_name': 'FoodRequest'},
            'cost_per_quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'desired_completion': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'quantity_type': ('django.db.models.fields.CharField', [], {'default': '(1, 1)', 'max_length': '3'}),
            'request_completed_bool': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'request_completed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'request_initiated': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['food']