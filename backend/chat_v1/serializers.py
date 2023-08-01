from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, HiddenField

from chat_v1.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений."""

    sender = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Message
        fields = ("sender", "receiver", "text")
        read_only_fields = ("sender",)

    def validate(self, attrs):
        if self.context["request"].user == attrs["receiver"]:
            raise ValidationError("Нельзя отправлять сообщения самому себе.")
        return attrs


class ListMessageSerializer(serializers.ModelSerializer):
    """Сериализатор ответа."""

    class Meta:
        model = Message
        fields = ("sender", "receiver", "text")
