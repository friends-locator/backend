from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from chat_v1.models import Message
from chat_v1.serializers import ListMessageSerializer, MessageSerializer


class SendMessage(CreateAPIView):
    """
    Создание записи с сообщением и получение последних 10 в ответе на
    POST-запрос.
    """

    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        query = Q(
            sender=request.user, receiver=self.request.data["receiver"]
        ) | Q(receiver=request.user, sender=self.request.data["receiver"])
        data = Message.objects.filter(query)[:10]
        serializer = ListMessageSerializer(
            data=data,
            many=True,
        )
        # TODO здесь трабла с ошибками сериализатора
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
