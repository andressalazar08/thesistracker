# Generated by Django 3.1.7 on 2021-04-07 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='estudiantes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('nombres', models.CharField(max_length=400)),
                ('apellidos', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='profesores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('nombres', models.CharField(max_length=400)),
                ('apellidos', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='tgrados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=400)),
                ('estado', models.CharField(choices=[('En desarrollo', 'En desarrollo'), ('Terminado', 'Terminado')], default='En desarrollo', max_length=100)),
                ('modalidad', models.CharField(choices=[('Monografía Diplomado', 'Monografía Diplomado'), ('Investigación Caso de Estudio', 'Investigación Caso de Estudio'), ('Emprendimiento Empresarial', 'Emprendimiento Empresarial')], default='Investigación Caso de Estudio', max_length=100)),
                ('cedula1', models.IntegerField()),
                ('nombre1', models.CharField(max_length=400)),
                ('apellidos1', models.CharField(max_length=400)),
                ('programa1', models.CharField(max_length=400)),
                ('cedula2', models.IntegerField(blank=True, null=True)),
                ('nombre2', models.CharField(blank=True, default='', max_length=400)),
                ('apellidos2', models.CharField(blank=True, default='', max_length=400)),
                ('programa2', models.CharField(blank=True, default='', max_length=400)),
                ('cedula3', models.IntegerField(blank=True, null=True)),
                ('nombre3', models.CharField(blank=True, default='', max_length=400)),
                ('apellidos3', models.CharField(blank=True, default='', max_length=400)),
                ('programa3', models.CharField(blank=True, default='', max_length=400)),
                ('fecha_asignacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='posteos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=500)),
                ('fecha_pub', models.DateField()),
                ('autor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trabajo_grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appusc.tgrados')),
            ],
            options={
                'ordering': ['-fecha_pub'],
            },
        ),
        migrations.CreateModel(
            name='comentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=400)),
                ('texto', models.TextField()),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_publicacion', models.DateTimeField(blank=True, null=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
