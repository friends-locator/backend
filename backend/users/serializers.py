from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.serializers import ValidationError

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
            "__all__"  # пока так, нужно обсудить какие поля будем возвращать
        )
