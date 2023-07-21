from re import match

from django.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)

from .models import CustomUser as User
from .models import FriendsCategory, FriendsRelationship


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "gender",
        )
        write_only_fields = ("password",)

    def validate_first_name(self, value):
        if not match(settings.NAME_REGEX_PATTERN, value):
            raise ValidationError("Некорректное имя пользователя.")
        return value

    def validate_last_name(self, value):
        if not match(settings.NAME_REGEX_PATTERN, value):
            raise ValidationError("Некорректная фамилия пользователя.")
        return value


class CustomUserSerializer(UserSerializer):
    """Кастомный сериализатор для работы с пользователем."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "longitude",
            "latitude",
        )


class FriendCategorySerializer(ModelSerializer):
    """Кастомный сериализатор для работы с категориями друзей."""
    class Meta:
        model = FriendsCategory
        fields = (
            "id",
            "name",
        )


class FriendsRelationshipSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с дружескими связями."""
    class Meta:
        model = FriendsRelationship
        fields = (
            "current_user",
            "friend",
            "friend_category",
        )


class FriendSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с друзьями."""
    friend_category = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "longitude",
            "latitude",
            "friend_category",
        )
        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "longitude",
            "latitude",
            "friend_category",
        )

    def get_friend_category(self, obj):
        friend_id = getattr(obj, "id")
        friend_data = FriendsRelationship.objects.get(friend_id=friend_id)
        category = FriendsCategory.objects.get(
            pk=friend_data.friend_category_id
        )
        return category.name


class CoordinateSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с координатами."""

    class Meta:
        model = User
        fields = (
            "longitude",
            "latitude",
        )

    def validate(self, data):
        if "longitude" not in data or "latitude" not in data:
            raise ValidationError(
                "Требуется передавать оба параметра широты и долготы."
            )
        return data
