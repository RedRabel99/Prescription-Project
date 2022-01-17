from django.db import models


# Create your models here.

class Drug(models.Model):
    name = models.CharField(max_length=150)
    form = models.CharField(max_length=100)
    dose = models.CharField(max_length=20)
    pack = models.CharField(max_length=100)
    fee = models.CharField(max_length=10)
    company = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
