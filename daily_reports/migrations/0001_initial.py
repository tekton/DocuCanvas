# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserDailyReport'
        db.create_table('daily_reports_userdailyreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('daily_reports', ['UserDailyReport'])

        # Adding model 'DailyReport'
        db.create_table('daily_reports_dailyreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('daily_reports', ['DailyReport'])


    def backwards(self, orm):
        # Deleting model 'UserDailyReport'
        db.delete_table('daily_reports_userdailyreport')

        # Deleting model 'DailyReport'
        db.delete_table('daily_reports_dailyreport')


    models = {
        'daily_reports.dailyreport': {
            'Meta': {'object_name': 'DailyReport'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'daily_reports.userdailyreport': {
            'Meta': {'object_name': 'UserDailyReport'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['daily_reports']