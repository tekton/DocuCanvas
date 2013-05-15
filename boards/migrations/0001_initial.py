# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Board'
        db.create_table(u'boards_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('height', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'boards', ['Board'])

        # Adding model 'BoardNote'
        db.create_table(u'boards_boardnote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boards.Board'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'boards', ['BoardNote'])

        # Adding model 'BoardNode'
        db.create_table(u'boards_boardnode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['boards.Board'])),
            ('nodeLink', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('x', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('y', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('nodeType', self.gf('django.db.models.fields.CharField')(default='note', max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'boards', ['BoardNode'])


    def backwards(self, orm):
        # Deleting model 'Board'
        db.delete_table(u'boards_board')

        # Deleting model 'BoardNote'
        db.delete_table(u'boards_boardnote')

        # Deleting model 'BoardNode'
        db.delete_table(u'boards_boardnode')


    models = {
        u'boards.board': {
            'Meta': {'object_name': 'Board'},
            'height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'boards.boardnode': {
            'Meta': {'object_name': 'BoardNode'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boards.Board']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nodeLink': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nodeType': ('django.db.models.fields.CharField', [], {'default': "'note'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'x': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'y': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'boards.boardnote': {
            'Meta': {'object_name': 'BoardNote'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['boards.Board']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['boards']