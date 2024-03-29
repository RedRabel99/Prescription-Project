from datetime import datetime, date

from rest_framework import serializers
from prescriptions.models import Prescription, PrescriptionSegment
from drugs.serializers import DrugSerializer
from prescriptions.tasks import send_email_task, get_prescription_email_content


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
        fields = ['id', 'segments', 'patient', 'doctor', 'realized', 'realization_date']
        read_only_fields = ['doctor', 'realization_date']

    def create(self, validated_data):
        segments = validated_data.pop('segments')
        prescription = Prescription.objects.create(**validated_data)
        for segment_data in segments:
            PrescriptionSegment.objects.create(prescription=prescription,
                                               **segment_data)
        try:
            content_string = get_prescription_email_content(prescription)

        except TypeError:
            content_string = "You have new prescription"
        title_string = 'New prescription has been prescribed to you'
        send_email_task.delay(title_string, content_string, [prescription.patient.email])

        return prescription

    def update(self, instance, validated_data):
        if instance.realized:
            raise serializers.ValidationError("This prescription is already realized")
        try:
            is_realized = validated_data['realized']
            if not is_realized:
                raise serializers.ValidationError("Cannot set realized field to False - it is already False")
            instance.realized = is_realized
            instance.realization_date = date.today()
            instance.save()
            return instance
        except KeyError:
            raise serializers \
                .ValidationError({'realized': ['This field is required',
                                               'To set prescription as realized you need to update it with ''realized '
                                               'field'' as True']})
