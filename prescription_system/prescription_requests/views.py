from django.shortcuts import render
from rest_framework.response import Response

from prescription_requests.serializers import PrescriptionRequestSerializer
from prescription_requests.models import PrescriptionRequest
from prescription_system.permissions import PrescriptionRequestPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, serializers, status


class PrescriptionRequestsViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionRequest.objects.all()
    serializer_class = PrescriptionRequestSerializer
    permission_classes = [IsAuthenticated, PrescriptionRequestPermission]
    authentication_classes = [JWTAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    def get_queryset(self):
        if self.request.user.is_patient:
            patient = self.request.user
            return PrescriptionRequest.objects.filter(patient=patient)
        elif self.request.user.is_doctor:
            doctor = self.request.user
            return PrescriptionRequest.objects.filter(doctor=doctor)

        return None

    def destroy(self, request, *args, **kwargs):
        prescription_request = self.get_object()
        if prescription_request.request_status not in ("PENDING", "pending"):
            return Response(
                {"message": "You cant delete request that has been accepted or denied"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        prescription_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

