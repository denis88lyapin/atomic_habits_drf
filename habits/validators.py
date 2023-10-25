from rest_framework.serializers import ValidationError
from datetime import timedelta


class RelatedHabitRewardValidator:
    def __init__(self, related_field, reward_field):
        self.related_field = related_field
        self.reward_field = reward_field

    def __call__(self, values):
        related_habit = values.get(self.related_field)
        reward = values.get(self.reward_field)

        if related_habit and reward:
            raise ValidationError({
                self.related_field: 'При выборе связанной привычки нельзя указывать вознаграждение!',
                self.reward_field: 'При выборе вознаграждения нельзя указывать связанную привычку!'
            })


class DurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_duration = value.get(self.field)
        if time_duration:
            if time_duration > timedelta(seconds=120):
                raise ValidationError(
                    {self.field: ['Время выполнения привычки должно быть не больше 120 секунд!']}
                )


class RelatedHabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        habit = value.get(self.field)
        if habit:
            if not habit.is_pleasant:
                raise ValidationError(
                    {self.field: ['В связанные привычки могут попадать только привычки с признаком приятной привычки!']}
                )


class IsPleasantValidator:
    def __init__(self, is_pleasant_field, related_field, reward_field):
        self.is_pleasant_field = is_pleasant_field
        self.related_field = related_field
        self.reward_field = reward_field

    def __call__(self, values):
        is_pleasant = values.get(self.is_pleasant_field)
        if is_pleasant:
            related_habit = values.get(self.related_field)
            reward = values.get(self.reward_field)
            if related_habit or reward:
                raise ValidationError(
                    {self.is_pleasant_field: [
                        'У приятной привычки не может быть вознаграждения или связанной привычки!']}
                )


class PeriodicityValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = value.get(self.field)
        if periodicity:
            if periodicity > 7:
                raise ValidationError(
                    {self.field: [
                        'Нельзя выполнять привычку реже, чем 1 раз в 7 дней!']}
                )
