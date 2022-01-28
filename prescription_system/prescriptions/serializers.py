from rest_framework import serializers
from prescriptions.models import Prescription, PrescriptionSegment
from drugs.serializers import DrugSerializer
from drugs.models import Drug


class PrescriptionSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionSegment
        fields = ['id', 'drug', 'count']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['drug'] = DrugSerializer(instance.drug).data
        return response


class PrescriptionSerializer(serializers.ModelSerializer):
    segments = PrescriptionSegmentSerializer(many=True)

    # drug = serializers.PrimaryKeyRelatedField(queryset=Drug.objects.all())

    class Meta:
        model = Prescription
        fields = ['id', 'segments', 'patient', 'doctor']
        read_only_fields = ['doctor']

    def create(self, validated_data):
        segments = validated_data.pop('segments')
        prescription = Prescription.objects.create(**validated_data)
        for segment_data in segments:
            PrescriptionSegment.objects.create(prescription=prescription,
                                               **segment_data)
        return prescription
