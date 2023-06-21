from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from users.serializers import CustomUserCreateSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователем."""

    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
