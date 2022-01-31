from datetime import datetime

from django.utils import timezone
from rest_framework import serializers
from prescription_requests.models import PrescriptionRequest, STATUS_CHOICES
from prescriptions.serializers import PrescriptionSegmentSerializer
from prescriptions.models import PrescriptionSegment


class PrescriptionRequestSerializer(serializers.ModelSerializer):
    segments = PrescriptionSegmentSerializer(many=True)
    #request_status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = PrescriptionRequest
        fields = ['id', 'segments', 'patient', 'doctor', 'request_status', 'decision_date']
        read_only_fields = ['patient', 'decision_date']

    def create(self, validated_data):
        segments = validated_data.pop('segments')

        prescription_request = PrescriptionRequest.objects.create(**validated_data)
        for segment_data in segments:
            PrescriptionSegment.objects.create(prescription_request=prescription_request,
                                               **segment_data)

        return prescription_request

    def update(self, instance, validated_data):
        request_status = validated_data.pop('request_status')
        if instance.request_status not in ('PENDING', 'pending'):
            raise serializers.ValidationError(f"Cant update request status, "
                                              f"current status: {instance.request_status}")
        instance.request_status = request_status
        instance.decision_date = timezone.now()
        instance.save()
        return instance
