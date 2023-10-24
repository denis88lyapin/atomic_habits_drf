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
            periodicity=2,
            reward='reward',
            duration='120',
        )

    def test_habit_list(self):
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
                    'date': str(datetime.now().date())
                }
            ]
        )

    def test_habit_create(self):
        url = reverse('habits:habit-list')
        data = {
            'user': self.user.pk,
            'place': 'home1',
            'time': '11:00:00',
            'action': 'action1',
            'reward': 'reward1',
            'duration': '45',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        habit = Habit.objects.all().last()
        self.assertEquals(
            {
                'id': habit.pk,
                'user': self.user.pk,
                'place': habit.place,
                'time': str(habit.time),
                'action': habit.action,
                'is_pleasant': habit.is_pleasant,
                'related_habit': habit.related_habit,
                'periodicity': habit.periodicity,
                'reward': habit.reward,
                'duration': str(habit.duration),
                'is_public': habit.is_public,
                'date': str(habit.date)
            },
            {
                'id': habit.pk,
                'user': self.user.pk,
                'place': 'home1',
                'time': '11:00:00',
                'action': 'action1',
                'is_pleasant': False,
                'related_habit': None,
                'periodicity': 1,
                'reward': 'reward1',
                'duration': '0:00:45',
                'is_public': False,
                'date': str(datetime.now().date())
            }
        )

    def test_habit_detail(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
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
                'date': str(datetime.now().date())
            }
        )

    def test_habit_update_PUT(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        data = {
            'place': self.habit.place,
            'time': '11:00:00',
            'action': 'action1',
            'reward': self.habit.reward,
            'duration': self.habit.duration,
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
            {
                'id': self.habit.pk,
                'user': self.user.pk,
                'place': 'home',
                'time': '11:00:00',
                'action': 'action1',
                'is_pleasant': False,
                'related_habit': None,
                'periodicity': 2,
                'reward': 'reward',
                'duration': '00:02:00',
                'is_public': False,
                'date': str(datetime.now().date())
            }
        )

    def test_habit_update_PATCH(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        data = {
            'time': '11:00:00',
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(
            response.json(),
            {
                'id': self.habit.pk,
                'user': self.user.pk,
                'place': 'home',
                'time': '11:00:00',
                'action': 'action',
                'is_pleasant': False,
                'related_habit': None,
                'periodicity': 2,
                'reward': 'reward',
                'duration': '00:02:00',
                'is_public': False,
                'date': str(datetime.now().date())
            }
        )

    def test_habit_delete(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.pk})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Habit.objects.all().exists(),
        )
