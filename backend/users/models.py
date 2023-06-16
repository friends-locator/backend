from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


from colorfield.fields import ColorField


class Status(models.Model):
    """Модель статуса пользователя"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Текст статуса",
        help_text="Введите статус",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", ]
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Tag(models.Model):
    """Модель интересов"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название",
        help_text="Введите название",
    )
    color = ColorField(unique=True, verbose_name="Цвет")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылка")

    class Meta:
        ordering = ["name", ]
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Основная модель пользователя"""

    GENDERS = ["Мужской", "Женский",]
    username_validator = UnicodeUsernameValidator()

    first_name = models.CharField(
        max_length=150, blank=True,
        verbose_name="Имя", help_text="Введите имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True,
        verbose_name="Фамилия", help_text="Введите фамилию"
    )
    email = models.EmailField(
        blank=True, verbose_name="E-mail", help_text="Введите ваш e-mail"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
        help_text="Введите логин",
        validators=[username_validator],
    )
    userpic = models.ImageField(
        upload_to="uploads/%Y/%m/%d/",
        validators=[FileExtensionValidator(
            allowed_extensions=["jpeg", "jpg", "png"])],
        verbose_name="Фото пользователя",
        help_text="Выберите изображение",
    )
    tags = models.ManyToManyField(
        Tag, related_name="tags",
        verbose_name="Интересы", help_text="Выберите интересы"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name="statuses",
        verbose_name="Статус",
        help_text="Укажите статус",
    )
    gender = models.CharField(
        max_length=50, choices=[GENDERS, ],
        verbose_name="Пол", help_text="Укажите ваш пол"
    )
    start_datetime = models.DateTimeField(auto_now_add=True)
    last_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
