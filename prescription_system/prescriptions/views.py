from django.shortcuts import render
from rest_framework import viewsets
from prescriptions.serializers import PrescriptionSerializer
from prescriptions.models import Prescription


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
