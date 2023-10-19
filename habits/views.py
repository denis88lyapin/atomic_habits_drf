from rest_framework import viewsets, generics
from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.permissions import IsOwnerOrSuperuser
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator
    permission_classes = [IsOwnerOrSuperuser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(user=self.request.user)


class ListPublicHabits(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitsPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
