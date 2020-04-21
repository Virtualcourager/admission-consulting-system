# Generated by Django 3.0.3 on 2020-03-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200323_1520'),
        ('adminsite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historyinfo',
            name='province',
        ),
        migrations.AddField(
            model_name='historyinfo',
            name='province',
            field=models.ManyToManyField(related_name='history_province', to='users.Province'),
        ),
    ]