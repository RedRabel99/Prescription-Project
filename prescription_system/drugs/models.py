from django.db import models


# Create your models here.

class Drug(models.Model):
    name = models.CharField(max_length=150)
    is_refunded = models.BooleanField(default=False)
