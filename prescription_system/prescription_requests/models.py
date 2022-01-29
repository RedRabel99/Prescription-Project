from django.db import models

from users.models import User

STATUS_CHOICES = (
    ("PENDING", "pending"),
    ("ACCEPTED", "accepted"),
    ("DENIED", "denied"),
)


class PrescriptionRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sent_prescription_request', null=True)
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='received_prescription_request',
                               null=True)
    request_status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=10)
    decision_date = models.DateTimeField(blank=True, null=True)
