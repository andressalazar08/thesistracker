# Generated by Django 3.1.7 on 2021-04-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appusc', '0010_auto_20210407_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posteos',
            name='fecha_pub',
            field=models.DateField(),
        ),
    ]
