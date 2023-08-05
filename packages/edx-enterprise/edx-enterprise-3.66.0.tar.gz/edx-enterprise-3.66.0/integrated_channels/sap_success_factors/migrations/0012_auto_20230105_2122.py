# Generated by Django 3.2.15 on 2023-01-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sap_success_factors', '0011_alter_sapsuccessfactorslearnerdatatransmissionaudit_index_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_content_sync_attempted_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent Content data record sync attempt', null=True),
        ),
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_content_sync_errored_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent failure of a Content data record sync attempt', null=True),
        ),
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_learner_sync_attempted_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent Learner data record sync attempt', null=True),
        ),
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_learner_sync_errored_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent failure of a Learner data record sync attempt', null=True),
        ),
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_sync_attempted_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent Content or Learner data record sync attempt', null=True),
        ),
        migrations.AddField(
            model_name='sapsuccessfactorsenterprisecustomerconfiguration',
            name='last_sync_errored_at',
            field=models.DateTimeField(blank=True, help_text='The DateTime of the most recent failure of a Content or Learner data record sync attempt', null=True),
        ),
    ]
