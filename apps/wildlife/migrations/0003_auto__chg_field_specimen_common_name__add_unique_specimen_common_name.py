# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Specimen.common_name'
        db.alter_column('wildlife_specimen', 'common_name', self.gf('django.db.models.fields.CharField')(default='Blah', unique=True, max_length=50))

        # Adding unique constraint on 'Specimen', fields ['common_name']
        db.create_unique('wildlife_specimen', ['common_name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Specimen', fields ['common_name']
        db.delete_unique('wildlife_specimen', ['common_name'])

        # Changing field 'Specimen.common_name'
        db.alter_column('wildlife_specimen', 'common_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))


    models = {
        'gpscollar.collar': {
            'Meta': {'object_name': 'Collar'},
            'collarID': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'wildlife.species': {
            'Meta': {'object_name': 'Species'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'wildlife.specimen': {
            'Meta': {'object_name': 'Specimen'},
            'age': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'collar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpscollar.Collar']", 'null': 'True', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wildlife.Species']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['wildlife']
