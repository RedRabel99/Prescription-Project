from django.db import models
from drugs.models import Drug
from django.core.validators import MinValueValidator


# Create your models here.

class Prescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class PrescriptionSegment(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    prescription = models.ForeignKey(Prescription, related_name="segments", on_delete=models.CASCADE)
