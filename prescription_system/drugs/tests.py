import json
from django.urls import reverse
from drugs.models import Drug
from users.models import User, Pharmacist
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
        self.test_drug = Drug.objects.create(**self.data)
        self.number_of_elements = 1
        self.list_url = reverse('drugs:drugs-list')

        self.user_data = {
            'username': 'pharmacist',
            'email': 'pharmacist@mail.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password': '1234',
            'user_type': 'PHARMACIST'
        }

        user = User.objects.create(**self.user_data)
        user.set_password(user.password)
        user.save()
        self.pharmacist = Pharmacist.objects.create(user=user, pharmacy='xD')
        self.pharmacist.save()

        login_response = self.client\
            .post(r'/token/', {'username': self.user_data['username'],
                               'password': self.user_data['password']}, format='json')
        token = json.loads(login_response.content)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_drug_create(self):
        response = self.client.post(self.list_url, self.data)
        queryset = Drug.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drug.objects.all().count(), self.number_of_elements + 1)

    def test_drug_list(self):
        response = self.client.get(self.list_url)
        queryset = Drug.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_drug_retrieve(self):
        response = self.client.get(reverse("drugs:drugs-detail", kwargs={"pk": self.test_drug.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_drug_update(self):
        response = self.client.patch(reverse("drugs:drugs-detail", kwargs={"pk": self.test_drug.id}),
                                     {"name": "newname", "dose": "30"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {
                             'id': self.test_drug.id,
                             'name': 'newname',
                             'form': 'pills',
                             'dose': '30',
                             'pack': '20',
                             'fee': '100%',
                             'company': 'test company\ntest addres 123'})

    def test_drug_delete(self):
        response = self.client.delete(reverse("drugs:drugs-detail", kwargs={"pk": self.test_drug.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Drug.objects.all().count(), self.number_of_elements - 1)
