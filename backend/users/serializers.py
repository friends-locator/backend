import base64
from re import match

from django.conf import settings
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ImageField, ModelSerializer,
                                        ValidationError)

from users.models import CustomUser as User


class Base64ImageField(ImageField):
    """Класс для добавления добавления аватара при создании пользователя."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


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


class UserpicSerializer(ModelSerializer):
    """Кастомный сериализатор для работы с аватаром пользователя."""

    user = HiddenField(default=CurrentUserDefault())
    userpic = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "user",
            "userpic",
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
