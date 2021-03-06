from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from users.models import User


class IsPharmacistOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.is_pharmacist


class PrescriptionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PUT', 'PATCH'):
            return request.user.is_pharmacist
        return request.user.is_doctor

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user == obj.patient:
                return True

        return request.user.is_doctor or request.user.is_pharmacist


class IsObjectOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor


class IsObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class PrescriptionRequestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_pharmacist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_patient or request.user.is_doctor

    def has_object_permission(self, request, view, obj):
        if request.user.is_pharmacist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return obj.patient == request.user or obj.doctor == request.user

        if request.method in ('PUT', 'PATCH'):
            return obj.doctor == request.user

        return request.user.is_patient


class IsPharmacist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_pharmacist
