from django.shortcuts import render
from users.serializers import DoctorSerializer, PatientSerializer, PharmacistSerializer
from users.models import Doctor, Patient, Pharmacist
from rest_framework import viewsets


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

