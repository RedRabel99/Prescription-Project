from prescription_system.permissions import IsDoctor, IsObject
from users.serializers import DoctorSerializer, PatientSerializer, PharmacistSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import Doctor, Patient, Pharmacist
from rest_framework import viewsets

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


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsDoctor, ]
        if self.action in OBJECT_ACTIONS:
            self.permission_classes = [IsAuthenticated, IsObject, ]
        return super(self.__class__, self).get_permissions()


class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ]
        if self.action == OBJECT_EDIT_ACTIONS:
            self.permission_classes = [IsAuthenticated, IsObject]
        return super(self.__class__, self).get_permissions()
