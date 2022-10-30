from rest_framework.decorators import action
from rest_framework.response import Response

from prescription_system.permissions import IsDoctor, IsObject, IsPharmacist, CanRetrieveGivenUserType
from users.serializers import DoctorSerializer, PatientSerializer, PharmacistSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.models import Doctor, Patient, Pharmacist, User
from rest_framework import viewsets, status, serializers, mixins

OBJECT_ACTIONS = ('retrieve', 'update', 'partial_update', 'destroy')
OBJECT_EDIT_ACTIONS = ('update', 'partial_update', 'destroy')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False, url_path='doctors')
    def doctor_list(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(user_type="DOCTOR")
        return self.list(request)

    @action(methods=['get'], detail=False, url_path='patients')
    def patient_list(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(user_type="PATIENT")
        return self.list(request)

    @action(methods=['get'], detail=False, url_path='pharmacists')
    def pharmacist_list(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(user_type="PHARMACIST")
        return self.list(request)

    def create(self, request, *args, **kwargs):
        register_type = request.query_params.get('user_type', 'PATIENT')
        print("wtf")
        request.data['user_type'] = register_type
        return super().create(request, *args, **kwargs)

    def get_object(self):
        if self.kwargs.get('pk', None) == 'current':
            self.kwargs['pk'] = self.request.user.id
        return super().get_object()

    def get_permissions(self):
        action_permissions = {
            "create": [AllowAny],
            "doctor_list": [IsAuthenticated],
            "pharmacist_list": [IsAdminUser],
            "patient_list": [IsAuthenticated, IsDoctor | IsAdminUser, ],
            "list": [IsAuthenticated, IsDoctor | IsPharmacist | IsAdminUser, ],
            "retrieve": [IsAuthenticated, IsObject | CanRetrieveGivenUserType, ],
            **dict.fromkeys(("update", "partial_update", "delete"), [IsAuthenticated, IsObject])
        }
        try:
            self.permission_classes = action_permissions[self.action]
        except KeyError:
            # In case some action isn't in action dict, allow only admin user for safety reason
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
