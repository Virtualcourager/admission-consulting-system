# Generated by Django 3.0.3 on 2020-04-07 14:24

from django.db import migrations, models
import material.models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultmaterial',
            name='file',
            field=models.FileField(default='files/default.default', upload_to=material.models.get_upload_file_name),
        ),
    ]
