# Generated by Django 3.0.3 on 2020-04-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_auto_20200408_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultmaterial',
            name='file',
            field=models.FileField(upload_to='image'),
        ),
    ]
