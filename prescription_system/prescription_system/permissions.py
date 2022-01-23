from rest_framework import permissions
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
        if request.method in ('PUT', 'PATCH') and not request.user.is_patient:
            return True
        return request.user.is_doctor

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user == obj.patient:
                return True

        return request.user.is_doctor or request.user.is_pharmacist
