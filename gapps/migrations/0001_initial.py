# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'createUser'
        db.create_table('gapps_createuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('admin_user', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin_pass', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('temp_pass', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('extension', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('gapps', ['createUser'])


    def backwards(self, orm):
        # Deleting model 'createUser'
        db.delete_table('gapps_createuser')


    models = {
        'gapps.createuser': {
            'Meta': {'object_name': 'createUser'},
            'admin_pass': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'admin_user': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'temp_pass': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['gapps']