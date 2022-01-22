from django.shortcuts import render
from rest_framework import viewsets
from drugs.serializers import DrugSerializer
from drugs.models import Drug


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
