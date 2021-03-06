# Generated by Django 3.2.11 on 2022-01-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription_requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptionrequest',
            name='request_status',
            field=models.CharField(blank=True, choices=[('PENDING', 'pending'), ('ACCEPTED', 'accepted'), ('DENIED', 'denied')], default='pending', max_length=10, null=True),
        ),
    ]
