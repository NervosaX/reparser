# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Detail'
        db.create_table(u'base_detail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('bedrooms', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bathrooms', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('carspaces', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pt_depart_time', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pt_arrive_time', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('pt_duration', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'base', ['Detail'])

        # Adding model 'RailwayPosition'
        db.create_table(u'base_railwayposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('detail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Detail'])),
            ('line_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('distance', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'base', ['RailwayPosition'])


    def backwards(self, orm):
        # Deleting model 'Detail'
        db.delete_table(u'base_detail')

        # Deleting model 'RailwayPosition'
        db.delete_table(u'base_railwayposition')


    models = {
        u'base.detail': {
            'Meta': {'object_name': 'Detail'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'bathrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bedrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'carspaces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'pt_arrive_time': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pt_depart_time': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pt_duration': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'base.railwayposition': {
            'Meta': {'object_name': 'RailwayPosition'},
            'detail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Detail']"}),
            'distance': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['base']