# Generated by Django 3.2.11 on 2022-01-29 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_patient_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]