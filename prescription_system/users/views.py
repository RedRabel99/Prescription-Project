from rest_framework.response import Response

from prescription_system.permissions import IsDoctor, IsObject, IsPharmacist
from users.serializers import DoctorSerializer, PatientSerializer, PharmacistSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import Doctor, Patient, Pharmacist
from rest_framework import viewsets, status, serializers, mixins

OBJECT_ACTIONS = ('retrieve', 'update', 'partial_update', 'destroy')
OBJECT_EDIT_ACTIONS = ('update', 'partial_update', 'destroy')


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [IsAuthenticated, ]
        if self.action in OBJECT_EDIT_ACTIONS:
            self.permission_classes = [IsAuthenticated, IsObject, ]
        return super(self.__class__, self).get_permissions()

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            if not self.request.user.is_doctor:
                raise serializers.ValidationError("Your account is not the doctor account")

            self.kwargs['pk'] = self.request.user.doctor_id.id
        return super(DoctorViewSet, self).get_object()


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsDoctor, ]
        if self.action in OBJECT_ACTIONS:
            self.permission_classes = [IsAuthenticated, IsObject, ]
        return super(self.__class__, self).get_permissions()

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            if not self.request.user.is_patient:
                raise serializers.ValidationError("Your account is not the patient account")
            self.kwargs['pk'] = self.request.user.patient_id.id
        return super(PatientViewSet, self).get_object()


class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            self.permission_classes = [IsAuthenticated, ]
            if not self.kwargs.get('pk', None) == 'me':
                self.permission_classes += [IsPharmacist, ]
        if self.action == OBJECT_EDIT_ACTIONS:
            self.permission_classes = [IsAuthenticated, IsObject]
        return super(self.__class__, self).get_permissions()

    def get_object(self):
        if self.kwargs.get('pk', None) == 'me':
            if not self.request.user.is_pharmacist:
                raise serializers.ValidationError("Your account is not the pharmacist account")
            self.kwargs['pk'] = self.request.user.pharmacist_id.id
        return super(PharmacistViewSet, self).get_object()

    def get_queryset(self):
        return Pharmacist.objects.filter(user=self.request.user)
