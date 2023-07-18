from re import match

from django.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import CustomUser as User


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


class FriendSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с друзьями."""

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
        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "longitude",
            "latitude",
        )


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
