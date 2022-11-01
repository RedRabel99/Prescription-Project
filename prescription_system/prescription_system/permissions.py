from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from users.models import User


class IsPharmacistOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.user_type == 'PHARMACIST'


class PrescriptionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PUT', 'PATCH'):
            return request.user.user_type == 'PHARMACIST'
        return request.user.user_type == 'DOCTOR'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user == obj.patient:
                return True

        return request.user.user_type in ['DOCTOR', 'PHARMACIST']


class IsObjectOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "DOCTOR"


class IsObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class PrescriptionRequestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'PHARMACIST':
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.user_type in ['DOCTOR', 'PATIENT']

    def has_object_permission(self, request, view, obj):
        if request.user.user_type == ['PHARMACIST']:
            return False

        if request.method in permissions.SAFE_METHODS:
            return obj.patient == request.user or obj.doctor == request.user

        if request.method in ('PUT', 'PATCH'):
            return obj.doctor == request.user

        return request.user.user_type == 'PATIENT'


class IsPharmacist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "PHARMACIST"


class CanRetrieveGivenUserType(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        object_type = obj.user_type
        user_type = request.user.user_type
        print(object_type)
        print(user_type)
        if object_type == 'DOCTOR':
            return True
        if object_type == 'PHARMACIST':
            return False
        if object_type == "PATIENT":
            return not user_type == "PATIENT"
        return request.user.is_staff
