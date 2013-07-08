# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FacebookProfile'
        db.create_table(u'socialplatform_facebookprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('profilePicture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'socialplatform', ['FacebookProfile'])

        # Adding model 'FBNotification'
        db.create_table(u'socialplatform_fbnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fb_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['socialplatform.FacebookProfile'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'socialplatform', ['FBNotification'])

        # Adding model 'TwitterProfile'
        db.create_table(u'socialplatform_twitterprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'socialplatform', ['TwitterProfile'])

        # Adding model 'Tweet'
        db.create_table(u'socialplatform_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'socialplatform', ['Tweet'])

        # Adding model 'DMAll'
        db.create_table(u'socialplatform_dmall', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'socialplatform', ['DMAll'])

        # Adding model 'DMIndividual'
        db.create_table(u'socialplatform_dmindividual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_ind_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('target_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['socialplatform.TwitterProfile'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'socialplatform', ['DMIndividual'])


    def backwards(self, orm):
        # Deleting model 'FacebookProfile'
        db.delete_table(u'socialplatform_facebookprofile')

        # Deleting model 'FBNotification'
        db.delete_table(u'socialplatform_fbnotification')

        # Deleting model 'TwitterProfile'
        db.delete_table(u'socialplatform_twitterprofile')

        # Deleting model 'Tweet'
        db.delete_table(u'socialplatform_tweet')

        # Deleting model 'DMAll'
        db.delete_table(u'socialplatform_dmall')

        # Deleting model 'DMIndividual'
        db.delete_table(u'socialplatform_dmindividual')


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
        u'socialplatform.dmall': {
            'Meta': {'object_name': 'DMAll'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'socialplatform.dmindividual': {
            'Meta': {'object_name': 'DMIndividual'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_ind_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'target_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['socialplatform.TwitterProfile']"})
        },
        u'socialplatform.facebookprofile': {
            'Meta': {'object_name': 'FacebookProfile'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'profilePicture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'socialplatform.fbnotification': {
            'Meta': {'object_name': 'FBNotification'},
            'fb_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['socialplatform.FacebookProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'socialplatform.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'socialplatform.twitterprofile': {
            'Meta': {'object_name': 'TwitterProfile'},
            'active': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['socialplatform']