import json
from django.urls import reverse
from drugs.models import Drug
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class DrugViewSetTestCase(APITestCase):
    def setUp(self):
        self.data = {
            'name': 'test drug',
            'form': 'pills',
            'dose': '500mg',
            'pack': '20',
            'fee': '100%',
            'company': 'test company\ntest addres 123'
        }
        Drug.objects.create(**self.data)
        self.number_of_elements = 1
        self.list_url = reverse('drugs:drugs-list')

        self.user_data = {
            'user': {
                'username': 'testuser',
                'first_name': 'name',
                'last_name': 'lastname',
                'email': 'mail@mail.com',
                'password': '1234',
                'is_pharmacist': True
            },
            'pharmacy': 'xD'
        }
        self.client.post(reverse('users:pharmacist-list'), self.user_data, format='json')
        login_response = self.client.post(r'/token/', {'username': 'testuser', 'password': '1234'}, format='json')
        token = json.loads(login_response.content)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_drug_create(self):
        response = self.client.post(self.list_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drug.objects.all().count(), self.number_of_elements + 1)

    def test_drug_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_drug_retrieve(self):
        response = self.client.get(reverse("drugs:drugs-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_drug_update(self):
        response = self.client.patch(reverse("drugs:drugs-detail", kwargs={"pk": 1}),
                                     {"name": "newname", "dose": "30"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {
                             'id': 1,
                             'name': 'newname',
                             'form': 'pills',
                             'dose': '30',
                             'pack': '20',
                             'fee': '100%',
                             'company': 'test company\ntest addres 123'})

    def test_drug_delete(self):
        response = self.client.delete(reverse("drugs:drugs-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Drug.objects.all().count(), self.number_of_elements - 1)
