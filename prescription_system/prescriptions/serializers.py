from rest_framework import serializers
from prescriptions.models import Prescription, PrescriptionSegment
from drugs.serializers import DrugSerializer


class PrescriptionSegmentSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)

    class Meta:
        model = PrescriptionSegment
        fields = ['id', 'drug', 'count']


class PrescriptionSerializer(serializers.ModelSerializer):
    segments = PrescriptionSegmentSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'segments']
        depth = 1
