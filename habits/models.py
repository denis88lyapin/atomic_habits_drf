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
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность выполнения в днях')
    reward = models.TextField(**NULLABLE, verbose_name='вознаграждение')
    duration = models.DurationField(verbose_name='продолжительность выполнения в минутах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    date = models.DateField(auto_now_add=True, verbose_name='дата и время последней отправки')

    def __str__(self):
        return f'Actin: {self.action}, time: {self.time}, period: {self.periodicity}'

    def habit_text(self):
        text = f'Задача: {self.action} в {self.time}. Продолжительность: {self.duration}.'
        text += f' Место: {self.place}.' if self.place else '.'
        if self.reward:
            text += f' Вознаграждение: {self.reward}.'
        return text

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
