# Generated by Django 2.2 on 2021-08-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innolla', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytime',
            name='small_groups',
            field=models.ManyToManyField(blank=True, help_text="Activitytime's small groups", related_name='activities', to='innolla.SmallGroup'),
        ),
        migrations.AlterField(
            model_name='activitytime',
            name='participants',
            field=models.ManyToManyField(blank=True, help_text="Activitytime's participants", related_name='activities', to='innolla.Profile'),
        ),
    ]