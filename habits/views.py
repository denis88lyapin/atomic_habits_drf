from rest_framework import viewsets

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    # permission_classes = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(user=self.request.user)