from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_id')
    specialization = models.TextField(max_length=50, null=True)


class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacist_id')
    pharmacy = models.TextField()


class Patient(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_id')
    address = models.TextField()
