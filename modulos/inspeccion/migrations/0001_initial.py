# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 14:47
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('propietario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inspeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servicio', models.CharField(choices=[('particular', 'Particular'), ('publico', 'P\xfablico'), ('especial', 'Especial')], default='particular', max_length=100)),
                ('kilometraje', models.CharField(blank=True, max_length=100, null=True)),
                ('paso', models.CharField(blank=True, choices=[('carga_documentos', 'Carga de documentos'), ('inspeccion_visual', 'Inspeccion Visual'), ('fotografias_vehiculo', 'Fotografias'), ('carga_analisis', 'Carga Analisis')], max_length=100, null=True)),
                ('finalizado', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('numero_inspeccion', models.IntegerField()),
                ('v_r_cliente', models.CharField(blank=True, max_length=100, null=True)),
                ('v_r_empresa', models.CharField(blank=True, max_length=100, null=True)),
                ('v_r_fasecolda', models.CharField(blank=True, max_length=100, null=True)),
                ('v_r_accesorios', models.CharField(blank=True, max_length=100, null=True)),
                ('propietario_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='propietario.PropietarioVehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('macro_value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('inspeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspeccion.Inspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionFotografia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_superior_derecha', models.ImageField(default='default/no-img.jpg', upload_to='uploads/inspeccion')),
                ('img_superior_izquierda', models.ImageField(default='default/no-img.jpg', upload_to='uploads/inspeccion')),
                ('img_delantera', models.ImageField(default='default/no-img.jpg', upload_to='uploads/inspeccion')),
                ('img_trasera', models.ImageField(default='default/no-img.jpg', upload_to='uploads/inspeccion')),
                ('img_interior', models.ImageField(default='default/no-img.jpg', upload_to='uploads/inspeccion')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inspeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspeccion.Inspeccion')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionImpronta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impronta', models.FileField(upload_to='uploads/improntas')),
                ('reated_at', models.DateTimeField(auto_now_add=True)),
                ('inspeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspeccion.Inspeccion')),
            ],
        ),
    ]
