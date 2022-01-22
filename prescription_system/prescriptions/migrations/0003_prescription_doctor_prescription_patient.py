# Generated by Django 4.0.1 on 2022-01-22 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prescriptions', '0002_alter_prescriptionsegment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issued_prescriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='patients_prescriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]
