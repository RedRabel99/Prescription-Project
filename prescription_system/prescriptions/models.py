from django.db import models
from drugs.models import Drug
from users.models import User
from django.core.validators import MinValueValidator


class Prescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='patients_prescriptions', null=True)
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='issued_prescriptions', null=True)


class PrescriptionSegment(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    prescription = models.ForeignKey(Prescription, related_name="segments", on_delete=models.CASCADE)
