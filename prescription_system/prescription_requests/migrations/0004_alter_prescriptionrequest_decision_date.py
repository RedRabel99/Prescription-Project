# Generated by Django 3.2.11 on 2022-01-29 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription_requests', '0003_alter_prescriptionrequest_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptionrequest',
            name='decision_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
