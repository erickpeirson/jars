# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-14 19:31
from __future__ import unicode_literals

import cookies.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('concepts', '0002_externalconcept_identityrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('hidden', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False, help_text=b'If a resource is not public it will only be accessible to logged-in users and will not appear in public search results. If this option is selected, you affirm that you have the right to upload and distribute this resource.')),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(help_text=b'You may provide your own URI, or allow the system to assign one automatically (recommended).', max_length=255, verbose_name=b'URI')),
                ('is_deleted', models.BooleanField(default=False)),
                ('indexable_content', models.TextField(blank=True, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
                ('content_resource', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, help_text=' Drop a file onto this field, or click "Choose File" to select a file on your computer. ', null=True, upload_to=cookies.models._resource_file_name)),
                ('location', models.URLField(blank=True, max_length=255, null=True, verbose_name=b'URL')),
            ],
            options={
                'abstract': False,
                'permissions': (('view_resource', 'View resource'), ('change_authorizations', 'Change authorizations'), ('view_authorizations', 'View authorizations')),
            },
        ),
        migrations.CreateModel(
            name='CollectionAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heritable', models.BooleanField(default=True, help_text=b'Policy applies to all resources in this collection.')),
                ('action', models.CharField(choices=[(b'VW', b'View'), (b'ED', b'Edit'), (b'AD', b'Add'), (b'RM', b'Remove'), (b'SH', b'Share')], max_length=2)),
                ('policy', models.CharField(choices=[(b'AL', b'Allow'), (b'DY', b'Deny')], max_length=2)),
                ('for_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorizations', to='cookies.Collection')),
                ('granted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_resource_auths', to=settings.AUTH_USER_MODEL)),
                ('granted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_resource_auths', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConceptEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('hidden', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False, help_text=b'If a resource is not public it will only be accessible to logged-in users and will not appear in public search results. If this option is selected, you affirm that you have the right to upload and distribute this resource.')),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(help_text=b'You may provide your own URI, or allow the system to assign one automatically (recommended).', max_length=255, verbose_name=b'URI')),
                ('is_deleted', models.BooleanField(default=False)),
                ('belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='native_conceptentities', to='cookies.Collection')),
                ('concept', models.ManyToManyField(blank=True, null=True, to='concepts.Concept')),
            ],
            options={
                'permissions': (('view_entity', 'View entity'), ('change_authorizations', 'Change authorizations'), ('view_authorizations', 'View authorizations')),
            },
        ),
        migrations.CreateModel(
            name='ContentRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(blank=True, max_length=100, null=True)),
                ('content_encoding', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'URI')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GilesToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=255)),
                ('for_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='giles_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GilesUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[(b'PD', b'Pending'), (b'EQ', b'Enqueued'), (b'ST', b'Sent'), (b'DO', b'Done'), (b'SE', b'Send error'), (b'GE', b'Giles error'), (b'PE', b'Process error'), (b'CE', b'Callback error')], max_length=2)),
                ('message', models.TextField()),
                ('on_complete', models.TextField()),
                ('file_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='giles_uploads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('entities', models.ManyToManyField(related_name='identities', to='cookies.ConceptEntity')),
                ('representative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='represents', to='cookies.ConceptEntity')),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('hidden', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False, help_text=b'If a resource is not public it will only be accessible to logged-in users and will not appear in public search results. If this option is selected, you affirm that you have the right to upload and distribute this resource.')),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(help_text=b'You may provide your own URI, or allow the system to assign one automatically (recommended).', max_length=255, verbose_name=b'URI')),
                ('is_deleted', models.BooleanField(default=False)),
                ('source_instance_id', models.PositiveIntegerField()),
                ('target_instance_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'metadata relation',
                'permissions': (('view_relation', 'View relation'), ('change_authorizations', 'Change authorizations'), ('view_authorizations', 'View authorizations')),
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('hidden', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False, help_text=b'If a resource is not public it will only be accessible to logged-in users and will not appear in public search results. If this option is selected, you affirm that you have the right to upload and distribute this resource.')),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(help_text=b'You may provide your own URI, or allow the system to assign one automatically (recommended).', max_length=255, verbose_name=b'URI')),
                ('is_deleted', models.BooleanField(default=False)),
                ('indexable_content', models.TextField(blank=True, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
                ('content_resource', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, help_text=' Drop a file onto this field, or click "Choose File" to select a file on your computer. ', null=True, upload_to=cookies.models._resource_file_name)),
                ('location', models.URLField(blank=True, max_length=255, null=True, verbose_name=b'URL')),
                ('is_part', models.BooleanField(default=False)),
                ('is_external', models.BooleanField(default=False)),
                ('external_source', models.CharField(blank=True, choices=[(b'GL', b'Giles'), (b'WB', b'Web')], max_length=2, null=True)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_resource', 'View resource'), ('change_authorizations', 'Change authorizations'), ('view_authorizations', 'View authorizations')),
            },
        ),
        migrations.CreateModel(
            name='ResourceAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[(b'VW', b'View'), (b'ED', b'Edit'), (b'SH', b'Share')], max_length=2)),
                ('policy', models.CharField(choices=[(b'AL', b'Allow'), (b'DY', b'Deny')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='containers', to=settings.AUTH_USER_MODEL)),
                ('part_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Collection')),
                ('primary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_primary_for', to='cookies.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_tags', to=settings.AUTH_USER_MODEL)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='cookies.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'URI')),
                ('active', models.BooleanField(default=True)),
                ('prefix', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('namespace', models.CharField(blank=True, max_length=255, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'URI')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('result_id', models.CharField(blank=True, max_length=255, null=True)),
                ('result', models.TextField()),
                ('progress', models.FloatField(default=0.0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_value', models.TextField()),
                ('_type', models.CharField(blank=True, max_length=255, null=True)),
                ('container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.ResourceContainer')),
            ],
        ),
        migrations.CreateModel(
            name='ConceptType',
            fields=[
                ('type_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cookies.Type')),
            ],
            bases=('cookies.type',),
        ),
        migrations.AddField(
            model_name='type',
            name='domain',
            field=models.ManyToManyField(blank=True, help_text=' The domain specifies the resource types to which this Type or Field can apply. If no domain is specified, then this Type or Field can apply to any resource. ', null=True, to='cookies.Type'),
        ),
        migrations.AddField(
            model_name='type',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='cookies.Type'),
        ),
        migrations.AddField(
            model_name='type',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='types', to='cookies.Schema'),
        ),
        migrations.AddField(
            model_name='resourcetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_tags', to='cookies.Tag'),
        ),
        migrations.AddField(
            model_name='resourceauthorization',
            name='for_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorizations', to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='resourceauthorization',
            name='granted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_collection_auths', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resourceauthorization',
            name='granted_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_collection_auths', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resource',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='resource',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resource',
            name='entity_type',
            field=models.ForeignKey(blank=True, help_text=b'Specifying a type helps to determine what metadata fields are appropriate for this resource, and can help with searching. Note that type-specific filtering of metadata fields will only take place after this resource has been saved.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Type', verbose_name=b'type'),
        ),
        migrations.AddField(
            model_name='resource',
            name='next_page',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_page', to='cookies.Resource'),
        ),
        migrations.AddField(
            model_name='relation',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='relation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='relation',
            name='entity_type',
            field=models.ForeignKey(blank=True, help_text=b'Specifying a type helps to determine what metadata fields are appropriate for this resource, and can help with searching. Note that type-specific filtering of metadata fields will only take place after this resource has been saved.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Type', verbose_name=b'type'),
        ),
        migrations.AddField(
            model_name='relation',
            name='predicate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='cookies.Field', verbose_name=b'field'),
        ),
        migrations.AddField(
            model_name='relation',
            name='source_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_from', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='relation',
            name='target_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relations_to', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='gilesupload',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='giles_uploads', to='cookies.Resource'),
        ),
        migrations.AddField(
            model_name='field',
            name='domain',
            field=models.ManyToManyField(blank=True, help_text=b'The domain specifies the resource types to which this Type or Field can apply. If no domain is specified, then this Type or Field can apply to any resource.', null=True, to='cookies.Type'),
        ),
        migrations.AddField(
            model_name='field',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='cookies.Field'),
        ),
        migrations.AddField(
            model_name='field',
            name='range',
            field=models.ManyToManyField(blank=True, help_text=" The field's range specifies the resource types that are valid values for this field. If no range is specified, then this field will accept any value. ", null=True, related_name='in_range_of', to='cookies.Type'),
        ),
        migrations.AddField(
            model_name='field',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='cookies.Schema'),
        ),
        migrations.AddField(
            model_name='contentrelation',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_relations', to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='contentrelation',
            name='content_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='cookies.Resource'),
        ),
        migrations.AddField(
            model_name='contentrelation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contentrelation',
            name='for_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='cookies.Resource'),
        ),
        migrations.AddField(
            model_name='conceptentity',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='conceptentity',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conceptentity',
            name='entity_type',
            field=models.ForeignKey(blank=True, help_text=b'Specifying a type helps to determine what metadata fields are appropriate for this resource, and can help with searching. Note that type-specific filtering of metadata fields will only take place after this resource has been saved.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Type', verbose_name=b'type'),
        ),
        migrations.AddField(
            model_name='collection',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.ResourceContainer'),
        ),
        migrations.AddField(
            model_name='collection',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='entity_type',
            field=models.ForeignKey(blank=True, help_text=b'Specifying a type helps to determine what metadata fields are appropriate for this resource, and can help with searching. Note that type-specific filtering of metadata fields will only take place after this resource has been saved.', null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Type', verbose_name=b'type'),
        ),
        migrations.AddField(
            model_name='collection',
            name='part_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookies.Collection'),
        ),
        migrations.AddField(
            model_name='concepttype',
            name='type_concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concepts.Type'),
        ),
    ]
