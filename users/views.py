from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [AllowAny]
    #     else:
    #         return super().get_permissions()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            instance = self.get_queryset().get(username=response.data['username'])
            password = request.data.get('password')
            if password:
                instance.set_password(password)
                instance.save()
        return response
