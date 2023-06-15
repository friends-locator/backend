from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# from colorfields.fields import ColorField


GENDERS = [("male", "Мужской"), ("female", "Женский")]


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    # color = ColorField(unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    userpic = models.ImageField(
        upload_to="users/",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png"])],
    )
    tags = models.ManyToManyField(Tag, related_name="tags")
    # status = models.ForeignKey(
    #     Status, on_delete=models.CASCADE, related_name="statuses"
    # )
    gender = models.CharField(choices=GENDERS, default="male", max_length=15,)
    start_datetime = models.DateTimeField(auto_now_add=True)
    last_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
