from rest_framework import viewsets
from drugs.serializers import DrugSerializer
from drugs.models import Drug
from prescription_system.permissions import IsPharmacistOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    permission_classes = [IsPharmacistOrReadOnly]
    authentication_classes = [JWTAuthentication,]
    serializer_class = DrugSerializer
