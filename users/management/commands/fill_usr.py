from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user1 = User.objects.create(
            username='test_1',
            is_active=True
        )
        user1.set_password('test1')
        user1.save()

        user2 = User.objects.create(
            username='test_2',
            is_active=True
        )
        user2.set_password('test2')
        user2.save()
