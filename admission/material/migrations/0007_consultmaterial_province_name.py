# Generated by Django 3.0.3 on 2020-04-10 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0006_auto_20200408_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultmaterial',
            name='province_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
