from django.db import models

from config import settings

NULLABLE = {
    'null': True,
    'blank': True
}


class Habit(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_SUNDAY = 'sunday'
    PERIOD_MONDAY = 'monday'
    PERIOD_TUESDAY = 'tuesday'
    PERIOD_WEDNESDAY = 'wednesday'
    PERIOD_THURSDAY = 'thursday'
    PERIOD_FRIDAY = 'friday'
    PERIOD_SATURDAY = 'saturday'

    PERIODS = (
        (PERIOD_DAILY, 'ежедневно'),
        (PERIOD_SUNDAY, 'воскресенье'),
        (PERIOD_MONDAY, 'понедельник'),
        (PERIOD_TUESDAY, 'вторник'),
        (PERIOD_WEDNESDAY, 'среда'),
        (PERIOD_THURSDAY, 'четверг'),
        (PERIOD_FRIDAY, 'пятница'),
        (PERIOD_SATURDAY, 'суббота'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=200, **NULLABLE, verbose_name='место выполнения')
    time = models.TimeField(auto_now_add=True, verbose_name='время начала выполнения')
    action = models.TextField(verbose_name='действие, которое представляет из себя привычка ')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='связанная привычка')
    periodicity = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY,
                                   verbose_name='периодичность выполнения')
    reward = models.TimeField(verbose_name='вознаграждение')
    duration = models.DurationField(verbose_name='продолжительность выполнения в минутах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
