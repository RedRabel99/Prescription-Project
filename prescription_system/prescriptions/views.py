from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from prescriptions.serializers import PrescriptionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from prescription_system.permissions import PrescriptionPermission
from prescriptions.models import Prescription
from users.models import User, Patient
from django.shortcuts import get_object_or_404


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    permission_classes = [IsAuthenticated, PrescriptionPermission]
    authentication_classes = [JWTAuthentication]
    serializer_class = PrescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def get_queryset(self):
        if not self.request.user.user_type == 'PATIENT':
            return Prescription.objects.all()
        try:
            patient = self.request.user
            patient_queryset = self.queryset.filter(patient=patient)
        except Patient.DoesNotExist:
            patient_queryset = Prescription.objects.none()
        return patient_queryset

    def partial_update(self, request, *args, **kwargs):
        prescription = get_object_or_404(Prescription,
                                         id=self.kwargs['pk'])

        if not prescription.realized:
            prescription.realized = True
            prescription.realization_date = datetime.now()
            prescription.save()
            return Response(
                {"message": "Prescription updated successfully"}, status=status.HTTP_201_CREATED
            )
        raise serializers.ValidationError('Prescription already realized')

