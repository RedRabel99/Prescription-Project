from django.db import models
from drugs.models import Drug


def validate_is_greater_than_zero(value):
    return value > 0


# Create your models here.

class Prescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class PrescriptionSegment(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    count = models.IntegerField(validators=[validate_is_greater_than_zero])
    prescription = models.ForeignKey(Prescription, related_name="segments", on_delete=models.CASCADE)
