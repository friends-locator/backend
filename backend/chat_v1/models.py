from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser as User


class Message(models.Model):
    """Модель сообщений"""

    sender = models.ForeignKey(
        User,
        verbose_name=_("Отправитель"),
        related_name="sending_user",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        verbose_name=_("Принимающий"),
        related_name="receiving_user",
        on_delete=models.CASCADE,
    )
    sending_datetime = models.DateTimeField(auto_now=True)
    text = models.TextField(
        max_length=1000,
        verbose_name=_("Текст сообщения"),
        help_text=_("Введите текст сообщения"),
    )

    class Meta:
        ordering = ("-sending_datetime",)
