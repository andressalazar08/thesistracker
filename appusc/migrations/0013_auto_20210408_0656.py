# Generated by Django 3.1.7 on 2021-04-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appusc', '0012_auto_20210408_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posteos',
            name='archivo',
            field=models.FileField(blank=True, default='', upload_to='postarchivos/'),
        ),
    ]
