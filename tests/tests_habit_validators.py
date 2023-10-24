from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from habits.models import Habit
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken


class HabitCRUDTestCase(APITestCase):
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
            is_pleasant=True,
            periodicity=2,
            duration='120',
        )

    def test_RelatedHabitRewardValidator_exception(self):
        url = reverse('habits:habit-list')
        data = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'related_habit': self.habit.pk,
            'reward': 'reward1',
            'duration': '45',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'related_habit': ['При выборе связанной привычки нельзя указывать вознаграждение!'],
             'reward': ['При выборе вознаграждения нельзя указывать связанную привычку!']}
        )

    def test_RelatedHabitRewardValidator(self):
        url = reverse('habits:habit-list')
        data = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'related_habit': self.habit.pk,
            'duration': '45',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        habit = Habit.objects.all().last()
        self.assertEquals(
            response.json(),
            {
                'id': habit.pk,
                'user': self.user.pk,
                'place': 'home1',
                'time': '11:00:00',
                'action': 'action1',
                'is_pleasant': False,
                'related_habit': self.habit.pk,
                'periodicity': 1,
                'reward': None,
                'duration': '00:00:45',
                'is_public': False,
                'date': str(habit.date)
            })

    def test_DurationValidator_exception(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        data = {
            'duration': 121,
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'duration': ['Время выполнения привычки должно быть не больше 120 секунд!']}
        )

    def test_RelatedHabitValidator_exception(self):
        self.habit.is_pleasant = False
        self.habit.save()
        url = reverse('habits:habit-list')
        data = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'related_habit': self.habit.pk,
            'duration': '45',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'related_habit': ['В связанные привычки могут попадать только привычки с признаком приятной привычки!']}
        )

    def test_IsPleasantValidator_exception(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        data = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'is_pleasant': True,
            'related_habit': self.habit.pk,
            'duration': '45',
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'is_pleasant': ['У приятной привычки не может быть вознаграждения или связанной привычки!']}
        )

        data_1 = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'is_pleasant': True,
            'reward': 'reward',
            'duration': '45',
        }
        response = self.client.patch(url, data_1)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'is_pleasant': ['У приятной привычки не может быть вознаграждения или связанной привычки!']}
        )

    def test_PeriodicityValidator_exception(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        data = {
            'periodicity': 8,
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.json(),
            {'periodicity': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней!']}
        )
