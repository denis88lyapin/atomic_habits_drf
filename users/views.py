from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from users.models import User
from users.permissions import IsUserOrSuperuser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOrSuperuser]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            instance = User.objects.filter(username=response.data['username']).first()
            password = request.data.get('password')
            if password:
                instance.set_password(password)
                instance.save()
        return response
