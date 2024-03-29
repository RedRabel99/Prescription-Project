import json
from django.urls import reverse
from rest_framework import status

from drugs.models import Drug
from prescriptions.models import Prescription, PrescriptionSegment
from users.models import User, Doctor, Patient, Pharmacist
from rest_framework.test import APITestCase


class PrescriptionTestCase(APITestCase):
    def setUp(self):
        self.doctor_user_data = {
            'username': 'doctor',
            'email': 'doctor@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'user_type': 'DOCTOR'
        }

        self.patient_user_data = {
            'username': 'patient',
            'email': 'patient@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'user_type': 'PATIENT'
        }

        self.pharmacist_user_data = {
            'username': 'pharmacist',
            'email': 'pharmacist@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'user_type': 'PHARMACIST'
        }

        self.drug_data = {
            'name': 'test drug',
            'form': 'pills',
            'dose': '500mg',
            'pack': '20',
            'fee': '100%',
            'company': 'test company\ntest addres 123'
        }

        doctor_user = User.objects.create(**self.doctor_user_data)
        doctor_user.set_password(doctor_user.password)
        doctor_user.save()
        self.doctor = Doctor.objects.create(user=doctor_user, specialization='doctor')
        self.doctor.save()

        patient_user = User.objects.create(**self.patient_user_data)
        patient_user.set_password(patient_user.password)
        patient_user.save()
        self.patient = Patient.objects.create(user=patient_user, address='XD')
        self.patient.save()

        pharmacist_user = User.objects.create(**self.pharmacist_user_data)
        pharmacist_user.set_password(pharmacist_user.password)
        pharmacist_user.save()
        self.pharmacist = Pharmacist.objects.create(user=pharmacist_user, pharmacy='xD')
        self.pharmacist.save()

        login_response = self.client.post('/token/', {'username': 'doctor', 'password': '1234'}, format='json')
        self.doctor_token = json.loads(login_response.content)['access']

        login_response = self.client.post('/token/', {'username': 'patient', 'password': '1234'}, format='json')
        self.patient_token = json.loads(login_response.content)['access']

        login_response = self.client.post('/token/', {'username': 'pharmacist', 'password': '1234'}, format='json')
        self.pharmacist_token = json.loads(login_response.content)['access']

        self.first_drug = Drug.objects.create(**self.drug_data)
        self.second_drug = Drug.objects.create(**self.drug_data)

        self.prescription = Prescription.objects.create(patient=self.patient.user, doctor=self.doctor.user)
        self.prescription.save()
        prescription_segment = PrescriptionSegment.objects.create(
            prescription=self.prescription, drug=self.first_drug, count=2
        )
        prescription_segment.save()
        self.prescription_count = Prescription.objects.all().count()

        self.list_url = reverse('prescriptions:prescription-list')

    def test_prescription_create(self):
        prescription_data = {
            'patient': self.patient.user.id,
            'segments': [
                {
                    "drug": self.first_drug.id,
                    "count": 4
                },
                {
                    "drug": self.second_drug.id,
                    "count": 7
                }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.post(self.list_url, prescription_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prescription.objects.all().count(), self.prescription_count + 1)
        self.assertEqual(json.loads(response.content)['doctor'], self.doctor.user.id)

    def test_prescription_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.patch(
            reverse("prescriptions:prescription-detail", kwargs={"pk": self.prescription.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.patch(
            reverse("prescriptions:prescription-detail", kwargs={"pk": self.prescription.id}),
            {'realized': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_prescriptions = Prescription.objects.get(id=self.prescription.id)
        self.assertEqual(updated_prescriptions.realized, True)
