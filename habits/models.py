from django.db import models

from config import settings

NULLABLE = {
    'null': True,
    'blank': True
}


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=200, **NULLABLE, verbose_name='место выполнения')
    time = models.TimeField(verbose_name='время начала выполнения')
    action = models.TextField(verbose_name='действие, которое представляет из себя привычка ')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='связанная привычка')
    periodicity = models.SmallIntegerField(default=1, verbose_name='периодичность выполнения в днях')
    reward = models.TextField(**NULLABLE, verbose_name='вознаграждение')
    duration = models.DurationField(verbose_name='продолжительность выполнения в минутах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'Actin: {self.action}, time: {self.time}, period: {self.periodicity}'

    def habit_text(self):
        text = f'Я буду {self.action} в {self.time}'
        text += f' в {self.action}.' if self.action else '.'
        return text

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
