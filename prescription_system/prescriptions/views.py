from django.shortcuts import render
from rest_framework import viewsets
from prescriptions.serializers import PrescriptionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from prescription_system.permissions import PrescriptionPermission
from prescriptions.models import Prescription
from users.models import User, Patient


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    permission_classes = [IsAuthenticated, PrescriptionPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = PrescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def get_queryset(self):
        if not self.request.user.is_patient:
            return Prescription.objects.all()
        try:
            patient = self.request.user
            patient_queryset = self.queryset.filter(patient=patient)
        except Patient.DoesNotExist:
            patient_queryset = Prescription.objects.none()
        return patient_queryset
