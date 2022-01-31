import json
from django.urls import reverse
from rest_framework import status

from drugs.models import Drug
from prescriptions.models import Prescription, PrescriptionSegment
from users.models import User, Doctor, Patient, Pharmacist
from rest_framework.test import APITestCase


class UsersTestCase(APITestCase):
    def setUp(self):
        self.doctor_user_data = {
            'username': 'doctor',
            'email': 'doctor@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'is_doctor': True
        }

        self.patient_user_data = {
            'username': 'patient',
            'email': 'patient@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'is_patient': True
        }

        self.pharmacist_user_data = {
            'username': 'pharmacist',
            'email': 'pharmacist@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'is_pharmacist': True
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

        self.patient_list_url = reverse('users:patient-list')
        self.doctor_list_url = reverse('users:doctor-list')
        self.pharmacist_list_url = reverse('users:pharmacist-list')

    def test_patient_create(self):
        new_patient_user_data = {
            'user': {
                'username': 'patient2',
                'email': 'patient2@mail.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password': '1234'
            },
            'address': 'XD'
        }
        response = self.client.post(self.patient_list_url, new_patient_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_response = self.client.post('/token/', {'username': 'patient2', 'password': '1234'}, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_doctor_create(self):
        new_doctor_user_data = {
            'user': {
                'username': 'doctor2',
                'email': 'doctor2@mail.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password': '1234'
            },
            'specialization': 'XD'
        }
        response = self.client.post(self.doctor_list_url, new_doctor_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_response = self.client.post('/token/', {'username': 'doctor2', 'password': '1234'}, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_pharmacist_create(self):
        new_pharmacist_user_data = {
            'user': {
                'username': 'pharmacist2',
                'email': 'pharmacist2@mail.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password': '1234'
            },
            'pharmacy': 'XD'
        }
        response = self.client.post(self.pharmacist_list_url, new_pharmacist_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_response = self.client.post('/token/', {'username': 'pharmacist2', 'password': '1234'}, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_doctor_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.get(self.patient_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(self.patient_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(self.patient_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pharmacist_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.get(self.pharmacist_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(self.pharmacist_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(self.pharmacist_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_request_patient(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.get(reverse('users:patient-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(reverse('users:patient-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_request_doctor(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(reverse('users:doctor-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(reverse('users:doctor-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_request_pharmacist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(reverse('users:pharmacist-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(reverse('users:pharmacist-detail', kwargs={'pk': 'me'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
