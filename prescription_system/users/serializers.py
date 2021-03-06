from rest_framework import serializers
from users.models import User, Doctor, Pharmacist, Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        if password is not None:
            user.set_password(password)
        user.is_doctor = True
        user.save()
        doctor, created = Doctor.objects.update_or_create(user=user, **validated_data)

        return doctor


class PharmacistSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Pharmacist
        fields = ['id', 'user', 'pharmacy']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        if password is not None:
            user.set_password(password)
        user.is_pharmacist = True
        user.save()
        pharmacist, created = Pharmacist.objects.update_or_create(user=user,
                                                                  pharmacy=validated_data.pop('pharmacy'))

        return pharmacist


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'address', 'birth_date']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        if password is not None:
            user.set_password(password)
        user.is_patient = True
        user.save()
        patient, created = Patient.objects.update_or_create(user=user,
                                                            address=validated_data.pop('address'),
                                                            birth_date=validated_data.pop('birth_date', None))

        return patient
