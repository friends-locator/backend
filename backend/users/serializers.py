from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer, ValidationError

User = get_user_model()


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
        if not match(r"[А-Яа-яA-Za-z ]+", value):
            raise ValidationError("Некорректное имя пользователя.")
        return value

    def validate_last_name(self, value):
        if not match(r"[А-Яа-яA-Za-z ]+", value):
            raise ValidationError("Некорректная фамилия пользователя.")
        return value

    def validate_password(self, value):
        if len(value) > 20:
            raise ValidationError("Слишком длинный пароль.")
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
        )

        read_only_fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )
