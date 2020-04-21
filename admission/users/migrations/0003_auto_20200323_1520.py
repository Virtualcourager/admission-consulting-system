# Generated by Django 3.0.3 on 2020-03-23 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='province',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Province'),
        ),
    ]