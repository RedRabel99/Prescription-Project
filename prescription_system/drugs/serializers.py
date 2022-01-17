from rest_framework.serializers import ModelSerializer
from drugs.models import Drug


class DrugsSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'form', 'dose', 'pack', 'fee', 'company']
