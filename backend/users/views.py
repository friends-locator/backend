from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from users.models import FriendsRelationship, FriendsRequest
from users.serializers import CustomUserSerializer, FriendSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет для работы с пользователем."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("tags",)
    search_fields = ("^email",)

    @action(detail=False)
    def friends(self, request):
        friends = request.user.friends.all()
        serializer = FriendSerializer(
            friends, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='add-friends'
    )
    def add_friend(self, request, **kwargs):
        current_user = request.user
        friend = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer = FriendSerializer(
            friend,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        FriendsRequest.objects.create(
            current_user=current_user,
            friend=friend
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def approved(self, request, **kwargs):
        friend = request.user
        current_user = get_object_or_404(User, id=self.kwargs.get('id'))
        serializer = FriendSerializer(
            current_user,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        FriendsRequest.objects.filter(
            current_user=current_user,
            friend=friend
        ).delete()
        current_user.friends.add(friend)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        methods=['delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def delete_friend(self, request, **kwargs):
        current_user = request.user
        friend = get_object_or_404(User, id=self.kwargs.get('id'))
        if not FriendsRelationship.objects.filter(
            current_user=current_user,
            friend=friend
        ).exists():
            return Response(
                {'errors': 'Пользователя нет в друзьях.'},
                status=HTTP_400_BAD_REQUEST
            )
        current_user.friends.remove(friend)
        return Response(status=HTTP_204_NO_CONTENT)
