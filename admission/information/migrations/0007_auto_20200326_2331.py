# Generated by Django 3.0.3 on 2020-03-26 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_auto_20200326_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='majorinfo',
            name='is_international',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='majorinfo',
            name='sciorart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='information.SciorArt'),
            preserve_default=False,
        ),
    ]