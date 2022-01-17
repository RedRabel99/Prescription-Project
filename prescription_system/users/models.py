from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


# Create your models here.

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_id')


class Pharmacist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacist_id')
