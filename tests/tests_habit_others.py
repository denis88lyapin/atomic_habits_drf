from datetime import datetime

from django.urls import exceptions
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from habits.models import Habit
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken


class HabitOthersTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test')
        self.user.set_password('test')
        self.user.save()

        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.habit = Habit.objects.create(
            user=self.user,
            place='home',
            time='12:00:00',
            action='action',
            periodicity=2,
            reward='reward',
            duration='120',
        )

    def test_habit_list_any_user(self):
        test_user = User.objects.create(username='Test1')
        test_user.set_password('test1')
        test_user.save()

        token = AccessToken.for_user(test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('habits:habit-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json().get('results'),
            []
        )

    def test_habit_list_superuser(self):
        test_user = User.objects.create(username='Test1', is_superuser=True)
        test_user.set_password('test1')
        test_user.save()

        token = AccessToken.for_user(test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('habits:habit-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json().get('results'),
            [
                {
                    'id': self.habit.pk,
                    'user': self.user.pk,
                    'place': 'home',
                    'time': '12:00:00',
                    'action': 'action',
                    'is_pleasant': False,
                    'related_habit': None,
                    'periodicity': 2,
                    'reward': 'reward',
                    'duration': '00:02:00',
                    'is_public': False,
                    'date': str(self.habit.date)
                }
            ]
        )

    def test_habit_list_any_user_1(self):
        self.habit.is_public = True
        self.habit.save()

        test_user = User.objects.create(username='Test1')
        test_user.set_password('test1')
        test_user.save()

        token = AccessToken.for_user(test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('habits:habits-public')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json().get('results'),
            [
                {
                    'id': self.habit.pk,
                    'user': self.user.pk,
                    'place': 'home',
                    'time': '12:00:00',
                    'action': 'action',
                    'is_pleasant': False,
                    'related_habit': None,
                    'periodicity': 2,
                    'reward': 'reward',
                    'duration': '00:02:00',
                    'is_public': True,
                    'date': str(self.habit.date)
                }
            ]
        )

    def test_habit_permissions_any_user(self):
        test_user = User.objects.create(username='Test1')
        test_user.set_password('test1')
        test_user.save()

        token = AccessToken.for_user(test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            response.json(),
            {'detail': 'Страница не найдена.'}
        )

    def test_habit_text(self):
        text = self.habit.habit_text()

        self.assertEquals(text,
                          'Задача: action в 12:00:00. Продолжительность: 120. '
                          'Место: home. Вознаграждение: reward.')

    def test_habit_str(self):
        self.assertEquals(self.habit.__str__(),
                          'Actin: action, time: 12:00:00, period: 2')
