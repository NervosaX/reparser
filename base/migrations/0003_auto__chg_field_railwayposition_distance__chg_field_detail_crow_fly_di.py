# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RailwayPosition.distance'
        db.alter_column(u'base_railwayposition', 'distance', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Detail.crow_fly_distance'
        db.alter_column(u'base_detail', 'crow_fly_distance', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Detail.estimated_speed'
        db.alter_column(u'base_detail', 'estimated_speed', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Detail.cable_length'
        db.alter_column(u'base_detail', 'cable_length', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):

        # Changing field 'RailwayPosition.distance'
        db.alter_column(u'base_railwayposition', 'distance', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Detail.crow_fly_distance'
        db.alter_column(u'base_detail', 'crow_fly_distance', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Detail.estimated_speed'
        db.alter_column(u'base_detail', 'estimated_speed', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Detail.cable_length'
        db.alter_column(u'base_detail', 'cable_length', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'base.detail': {
            'Meta': {'object_name': 'Detail'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'bathrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bedrooms': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cable_length': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'carspaces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'crow_fly_distance': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'estimated_speed': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
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
            'distance': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['base']