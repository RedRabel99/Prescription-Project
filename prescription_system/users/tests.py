import json
from django.urls import reverse
from rest_framework import status
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

        self.admin_data = {
            'username': 'admin',
            'email': 'admin@mail',
            'password': 'admin'
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

        self.admin_user = User.objects.create_superuser(**self.admin_data)
        self.admin_user.save()

        login_response = self.client.\
            post('/token/', {'username': self.doctor_user_data['username'],
                             'password': self.doctor_user_data['password']})
        self.doctor_token = json.loads(login_response.content)['access']

        login_response = self.client.\
            post('/token/', {'username': self.patient_user_data['username'],
                             'password': self.patient_user_data['password']})
        self.patient_token = json.loads(login_response.content)['access']

        login_response = self.client.\
            post('/token/', {'username': self.pharmacist_user_data['username'],
                             'password': self.pharmacist_user_data['password']})
        self.pharmacist_token = json.loads(login_response.content)['access']

        login_response = self.client.\
            post('/token/', {'username': self.admin_data['username'],
                             'password': self.admin_data['password']})
        self.admin_token = json.loads(login_response.content)['access']

        self.patient_list_url = reverse('users:user-patient-list')
        self.doctor_list_url = reverse('users:user-doctor-list')
        self.pharmacist_list_url = reverse('users:user-pharmacist-list')
        self.user_list_url = reverse('users:user-list')
        self.user_current_detail_url = reverse('users:user-detail', kwargs={'pk': 'current'})

    def test_patient_create(self):
        new_patient_user_data = {
            'username': 'patient2',
            'email': 'patient2@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'patient_id': {
                'address': 'XD'
            }
        }

        response = self.client.post(self.user_list_url, new_patient_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_response = self.client\
            .post('/token/', {'username': new_patient_user_data['username'],
                              'password': new_patient_user_data['password']})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_doctor_create(self):
        new_doctor_user_data = {
            'username': 'doctor2',
            'email': 'doctor2@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'doctor_id': {
                'specialization': 'XD'
            }
        }

        response = self.client.post(self.user_list_url + '?user_type=DOCTOR', new_doctor_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.\
            post('/token/', {'username': new_doctor_user_data['username'],
                             'password': new_doctor_user_data['password']})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_pharmacist_create(self):
        new_pharmacist_user_data = {
            'username': 'pharmacist2',
            'email': 'pharmacist2@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'pharmacist_id': {
                'pharmacy': 'XD'
            }
        }

        response = self.client\
            .post(self.user_list_url + '?user_type=PHARMACIST', new_pharmacist_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_response = self.client\
            .post('/token/', {'username': new_pharmacist_user_data['username'],
                              'password': new_pharmacist_user_data['password']})
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.pharmacist_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.get(self.user_current_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['user_type'], 'PATIENT')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.get(self.user_current_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['user_type'], 'DOCTOR')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.get(self.user_current_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['user_type'], 'PHARMACIST')