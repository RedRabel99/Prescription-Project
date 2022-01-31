import json
from django.urls import reverse
from rest_framework import status

from drugs.models import Drug
from prescriptions.models import Prescription, PrescriptionSegment
from prescription_requests.models import PrescriptionRequest
from users.models import User, Doctor, Patient, Pharmacist
from rest_framework.test import APITestCase


class PrescriptionRequestTestCase(APITestCase):

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

        self.first_drug = Drug.objects.create(**self.drug_data)
        self.second_drug = Drug.objects.create(**self.drug_data)

        self.prescription_request = PrescriptionRequest.objects.create(patient=self.patient.user,
                                                                       doctor=self.doctor.user)
        self.prescription_request.save()

        self.accepted_prescription_request = PrescriptionRequest.objects.create(patient=self.patient.user,
                                                                                doctor=self.doctor.user,
                                                                                request_status='ACCEPTED') 
        self.accepted_prescription_request.save()
        
        first_prescription_segment = PrescriptionSegment.objects.create(
            prescription_request=self.prescription_request, drug=self.first_drug, count=2
        )
        first_prescription_segment.save()

        accepted_prescription_segment = PrescriptionSegment.objects.create(
            prescription_request=self.prescription_request, drug=self.first_drug, count=2
        )
        accepted_prescription_segment.save()
        self.prescription_request_count = PrescriptionRequest.objects.all().count()

        self.list_url = reverse('prescription-requests:prescriptionrequest-list')

    def test_prescription_request_create(self):
        prescription_request_data = {
            'doctor': self.doctor.user.id,
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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.post(self.list_url, prescription_request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrescriptionRequest.objects.all().count(), self.prescription_request_count + 1)
        self.assertEqual(json.loads(response.content)['patient'], self.patient.user.id)

    def test_accept_prescription_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.patient_token)
        response = self.client.patch(
            reverse('prescription-requests:prescriptionrequest-detail',
                    kwargs={'pk': self.prescription_request.id}), {'request_status': 'accepted'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.patch(
            reverse('prescription-requests:prescriptionrequest-detail',
                    kwargs={'pk': self.prescription_request.id}), {'request_status': 'ACCEPTED'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_prescription_request = PrescriptionRequest.objects.get(id=self.prescription_request.id)
        self.assertEqual(updated_prescription_request.request_status, 'ACCEPTED')

    def test_deny_prescription_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.pharmacist_token)
        response = self.client.patch(
            reverse('prescription-requests:prescriptionrequest-detail',
                    kwargs={'pk': self.prescription_request.id}), {'request_status': 'accepted'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.patch(
            reverse('prescription-requests:prescriptionrequest-detail',
                    kwargs={'pk': self.prescription_request.id}), {'request_status': 'DENIED'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_prescription_request = PrescriptionRequest.objects.get(id=self.prescription_request.id)
        self.assertEqual(updated_prescription_request.request_status, 'DENIED')

    def test_update_not_pending_prescription_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.doctor_token)
        response = self.client.patch(
            reverse('prescription-requests:prescriptionrequest-detail',
                    kwargs={'pk': self.accepted_prescription_request.id}), {'request_status': 'DENIED'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
