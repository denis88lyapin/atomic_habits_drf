from rest_framework import serializers
from habits.models import Habit
from habits.validators import RelatedHabitRewardValidator, DurationValidator, PeriodicityValidator, \
    RelatedHabitValidator, IsPleasantValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'id', 'user', 'place', 'time', 'action', 'is_pleasant', 'related_habit', 'periodicity', 'reward',
            'duration', 'is_public', 'date')
        read_only_fields = ('user', 'last_try',)
        validators = [
            RelatedHabitRewardValidator('related_habit', 'reward'),
            DurationValidator('duration'),
            RelatedHabitValidator('related_habit'),
            IsPleasantValidator('is_pleasant', 'related_habit', 'reward'),
            PeriodicityValidator('periodicity')
        ]
