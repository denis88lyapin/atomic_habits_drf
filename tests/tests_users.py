from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken


class HabitCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test')
        self.user.set_password('test')
        self.user.save()
        self.token = AccessToken.for_user(self.user)

        self.user_2 = User.objects.create(username='Test_2', is_superuser=True)
        self.user_2.set_password('test_2')
        self.user_2.save()
        self.token_2 = AccessToken.for_user(self.user_2)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_users_list(self):
        url = reverse('users:profile-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        username = response.json()[0].get('username')
        password = response.json()[0].get('password')
        self.assertEquals(self.user.username, username)
        self.assertEquals(self.user.password, password)

    def test_users_create(self):
        url = reverse('users:profile-list')
        data = {
            'username': 'Test_3',
            'password': 'test_3'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        username = response.json().get('username')
        password = response.json().get('password')
        self.assertEquals(data['username'], username)
        self.assertEquals(data['password'], password)

    def test_users_list_superuser(self):
        url = reverse('users:profile-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_2}')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(2, len(response.json()))

    def test_users_detail(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        username = response.json().get('username')
        password = response.json().get('password')
        self.assertEquals(self.user.username, username)
        self.assertEquals(self.user.password, password)

    def test_users_detail_superuser(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_2}')
        response = self.client.get(url)
        username = response.json().get('username')
        password = response.json().get('password')
        self.assertEquals(self.user.username, username)
        self.assertEquals(self.user.password, password)

    def test_users_detail_any_user(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.user_2.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            response.json(),
            {'detail': 'Страница не найдена.'}
        )

    def test_users_update(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.user.pk})
        data = {
            'first_name': 'Test_Test'
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        updated_user = User.objects.get(pk=self.user.pk)

        self.assertEquals(updated_user.username, self.user.username)
        self.assertEquals(updated_user.password, self.user.password)
        self.assertEquals(updated_user.first_name, data['first_name'])

    def test_users_delete(self):
        url = reverse('users:profile-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(
            User.objects.filter(pk=self.user.pk).first(), None
        )

    def test_user_str(self):
        self.assertEquals(self.user.__str__(), 'Test')
