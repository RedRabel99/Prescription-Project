from django.shortcuts import render
from rest_framework import viewsets
from drugs.serializers import DrugsSerializer
from drugs.models import Drug


class DrugsModelViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugsSerializer
