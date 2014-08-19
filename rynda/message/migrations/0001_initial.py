# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'message_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_column='name')),
            ('description', self.gf('django.db.models.fields.TextField')(db_column='description', blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_column='slug', blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(db_column='order')),
        ))
        db.send_create_signal(u'message', ['Category'])

        # Adding model 'Message'
        db.create_table(u'message_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('additional_info', self.gf('jsonfield.fields.JSONField')(default='', blank=True)),
            ('messageType', self.gf('django.db.models.fields.IntegerField')(db_column='message_type')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], db_column='user_id')),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('is_virtual', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_important', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_feedback', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1, null=True, blank=True)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_column='date_add', blank=True)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_column='date_modify', blank=True)),
            ('expired_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('edit_key', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('sender_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('linked_location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geozones.Location'], null=True, blank=True)),
        ))
        db.send_create_signal(u'message', ['Message'])

        # Adding M2M table for field category on 'Message'
        m2m_table_name = db.shorten_name(u'message_message_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'message.message'], null=False)),
            ('category', models.ForeignKey(orm[u'message.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'category_id'])

        # Adding model 'MessageNotes'
        db.create_table(u'message_messagenotes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['message.Message'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'message', ['MessageNotes'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'message_category')

        # Deleting model 'Message'
        db.delete_table(u'message_message')

        # Removing M2M table for field category on 'Message'
        db.delete_table(db.shorten_name(u'message_message_category'))

        # Deleting model 'MessageNotes'
        db.delete_table(u'message_messagenotes')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geozones.location': {
            'Meta': {'object_name': 'Location'},
            'coordinates': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Location'", 'max_length': '250'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Region']", 'null': 'True', 'blank': 'True'})
        },
        u'geozones.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'message.category': {
            'Meta': {'ordering': "['order']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'db_column': "'description'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'name'"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'order'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_column': "'slug'", 'blank': 'True'})
        },
        u'message.message': {
            'Meta': {'ordering': "['-date_add']", 'object_name': 'Message'},
            'additional_info': ('jsonfield.fields.JSONField', [], {'default': "''", 'blank': 'True'}),
            'allow_feedback': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['message.Category']", 'null': 'True', 'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'date_add'", 'blank': 'True'}),
            'edit_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'expired_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_virtual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'date_modify'", 'blank': 'True'}),
            'linked_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Location']", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'messageType': ('django.db.models.fields.IntegerField', [], {'db_column': "'message_type'"}),
            'sender_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'db_column': "'user_id'"})
        },
        u'message.messagenotes': {
            'Meta': {'object_name': 'MessageNotes'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['message.Message']"}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['message']