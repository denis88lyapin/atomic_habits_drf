from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet, ListPublicHabits

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('habits/public/', ListPublicHabits.as_view(), name='habits-public'),
] + router.urls
