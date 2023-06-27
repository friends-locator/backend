from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from users.serializers import CustomUserSerializer, FriendSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователем."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("tags",)

    @action(detail=False)
    def friends(self, request):
        friends = request.user.friends.all()
        serializer = FriendSerializer(
            friends, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)
