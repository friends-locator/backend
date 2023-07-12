import requests
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
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
        methods=["post"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="add-friend",
    )
    def add_friend(self, request, **kwargs):
        from_user = request.user
        to_user = get_object_or_404(User, id=self.kwargs.get("id"))
        serializer = FriendSerializer(
            to_user, data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        if FriendsRequest.objects.filter(
            from_user=to_user, to_user=from_user
        ).exists():
            FriendsRequest.objects.filter(
                from_user=to_user, to_user=from_user
            ).delete()
            from_user.friends.add(to_user)
        else:
            FriendsRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="approved",
    )
    def approve_request(self, request, **kwargs):
        to_user = request.user
        from_user = get_object_or_404(User, id=self.kwargs.get("id"))
        serializer = FriendSerializer(
            from_user, data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        if not FriendsRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            return Response(
                {"errors": "Такой заявки нет."}, status=HTTP_400_BAD_REQUEST
            )
        FriendsRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).delete()
        from_user.friends.add(to_user)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        methods=["delete"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="delete-friend",
    )
    def delete_friend(self, request, **kwargs):
        current_user = request.user
        friend = get_object_or_404(User, id=self.kwargs.get("id"))
        if not FriendsRelationship.objects.filter(
            current_user=current_user, friend=friend
        ).exists():
            return Response(
                {"errors": "Пользователя нет в друзьях."},
                status=HTTP_400_BAD_REQUEST,
            )
        current_user.friends.remove(friend)
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=["delete"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="delete-request",
    )
    def delete_request(self, request, **kwargs):
        from_user = request.user
        to_user = get_object_or_404(User, id=self.kwargs.get("id"))
        if not FriendsRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            return Response(
                {"errors": "Такой заявки не существует."},
                status=HTTP_400_BAD_REQUEST,
            )
        FriendsRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="all-requests",
    )
    def all_requests(self, request):
        all_requests = User.objects.filter(user__to_user=request.user)
        serializer = FriendSerializer(
            all_requests, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=["put"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="update-position",
    )
    def update_position(self, request, **kwargs):
        user = request.user
        serializer = CustomUserSerializer(
            user,
            data=request.data,
            longitude=self.kwargs.get("longitude"),
            latitude=self.kwargs.get("latitude"),
            context={"request": request},
        )
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="get-friends",
    )
    def get_friends(self, request, **kwargs):
        user = request.user
        start_longitude = (self.kwargs.get("start_longitude"),)
        start_latitude = (self.kwargs.get("start_latitude"),)
        end_longitude = (self.kwargs.get("end_longitude"),)
        end_latitude = (self.kwargs.get("end_latitude"),)
        longitude = (self.kwargs.get("longitude"),)
        latitude = (self.kwargs.get("latitude"),)
        nearby_friends = FriendsRequest.objects.filter(
            longitude in [start_longitude, end_longitude],
            latitude in [start_latitude, end_latitude],
            user=user,
        )
        serializer = FriendSerializer(
            user,
            nearby_friends,
            data=request.data,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)


class ActivateUserView(GenericAPIView):
    """Подтверждение мейла."""

    permission_classes = [AllowAny]

    def get(self, request, uid, token, format=None):
        """Отправка POST вместо GET."""
        payload = {"uid": uid, "token": token}
        actiavtion_url = "http://localhost:8000/api/v1/users/activation/"
        response = requests.post(actiavtion_url, data=payload)
        if response.status_code == 204:
            return Response({}, response.status_code)
        return Response(response.json())
