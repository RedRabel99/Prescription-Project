from rest_framework import serializers
from users.models import User, Doctor, Pharmacist, Patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization']


class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['pharmacy']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['address', 'birth_date']


class UserSerializer(serializers.ModelSerializer):
    doctor_id = DoctorSerializer(required=False)
    patient_id = PatientSerializer(required=False)
    pharmacist_id = PharmacistSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password',
                  'doctor_id', 'patient_id', 'pharmacist_id', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print("Dupsko")
        user_type = validated_data['user_type']
        if user_type.lower() == 'admin':
            raise serializers.ValidationError({"user_type": ["admin is not a valid choice"]})
        doctor_id_data = validated_data.pop('doctor_id', None)
        patient_id_data = validated_data.pop('patient_id', None)
        pharmacist_id_data = validated_data.pop('pharmacist_id', None)
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
        if user_type.lower() == "patient":
            try:
                patient_id_data['user'] = user
                patient = PatientSerializer.create(PatientSerializer(), validated_data=patient_id_data)
                patient.save()
            except TypeError:
                user.delete()
                raise serializers.ValidationError({"patient_id": ["This field is required"]})
        if user_type.lower() == "doctor":
            try:
                doctor_id_data['user'] = user
                doctor = DoctorSerializer.create(DoctorSerializer(), validated_data=doctor_id_data)
                doctor.save()
            except TypeError:
                user.delete()
                raise serializers.ValidationError({"doctor_id": ["This field is required"]})
        if user_type.lower() == "pharmacist":

            try:
                pharmacist_id_data['user'] = user
                pharmacist = PharmacistSerializer.create(PharmacistSerializer(), validated_data=pharmacist_id_data)
                pharmacist.save()
            except TypeError:
                user.delete()
                raise serializers.ValidationError({"pharmacist_id": ["This field is required"]})
        user.save()
        return user

    def update(self, instance, validated_data):

        if instance.user_type.lower() == "patient":
            nested_instance = instance.patient_id
            nested_data = validated_data.pop('patient_id')
            PatientSerializer.update(PatientSerializer(), instance=nested_instance, validated_data=nested_data)
        if instance.user_type.lower() == "doctor":
            nested_instance = instance.doctor_id
            nested_data = validated_data.pop('doctor_id')
            DoctorSerializer.update(DoctorSerializer(), instance=nested_instance, validated_data=nested_data)
        if instance.user_type.lower() == "pharmacist":
            nested_instance = instance.pharmacist_id
            nested_data = validated_data.pop('pharmacist_id')
            PharmacistSerializer.update(PharmacistSerializer(), instance=nested_instance, validated_data=nested_data)

        return super(UserSerializer, self).update(instance, validated_data)
