from re import match

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ValidationError


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания Пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'gender'
        )
        write_only_fields = ('password',)

    def validate_username(self, value):
        if not match(r'[\w.@+\-]+', value):
            raise ValidationError('Некорректный логин')
        return value

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Такой электронный адрес уже существует.')
        return email


# class UserPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(
#         label='Новый пароль')
#     current_password = serializers.CharField(
#         label='Текущий пароль')

#     def validate_current_password(self, current_password):
#         user = self.context['request'].user
#         if not authenticate(
#                 username=user.email,
#                 password=current_password):
#             raise serializers.ValidationError(
#                 ERR_MSG, code='authorization')
#         return current_password

#     def validate_new_password(self, new_password):
#         validators.validate_password(new_password)
#         return new_password

#     def create(self, validated_data):
#         user = self.context['request'].user
#         password = make_password(
#             validated_data.get('new_password'))
#         user.password = password
#         user.save()
#         return validated_data
