from colorfield.fields import ColorField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Модель статуса пользователя."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Текст статуса"),
        help_text=_("Введите статус"),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("Статус")
        verbose_name_plural = _("Статусы")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель интересов."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Название"),
        help_text=_("Введите название"),
    )
    color = ColorField(unique=True, verbose_name=_("Цвет"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))

    class Meta:
        ordering = ("name",)
        verbose_name = _("Интерес")
        verbose_name_plural = _("Интересы")

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер юзеров."""

    def create_user(self, email, username, role=None, password=None, **others):
        if not email:
            raise ValueError(_("У пользователя должен быть указан email"))

        validate_password(password)

        user = self.model(
            email=self.normalize_email(email), username=username, **others
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **others):
        user = self.model(email=self.normalize_email(email), username=username)
        user.is_superuser = True
        user.is_staff = True
        # Суперюзер заведомо будет иметь фиксированный статус
        # Создание возможно только после добавления статуса
        # На момент разработки оставлю заглушку:
        Status.objects.get_or_create(id=1)  # Удалить после разработки
        user.status_id = 1
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """Основная модель пользователя."""

    MALE = "male"
    FEMALE = "female"
    ROLE_CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский"),
    ]

    username_validator = UnicodeUsernameValidator()
    objects = CustomUserManager()

    first_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Имя"),
        help_text=_("Введите имя"),
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Фамилия"),
        help_text=_("Введите фамилию"),
    )
    email = models.EmailField(
        verbose_name=_("E-mail"),
        help_text=_("Введите ваш e-mail"),
        unique=True,
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Логин"),
        help_text=_("Введите логин"),
        validators=[username_validator],
    )
    userpic = models.ImageField(
        upload_to="uploads/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png"])
        ],
        verbose_name=_("Фото пользователя"),
        help_text=_("Выберите изображение"),
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name=_("Интересы"),
        help_text=_("Выберите интересы"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        related_name="statuses",
        verbose_name=_("Статус"),
        help_text=_("Укажите статус"),
        default=1,
        null=True,
    )
    gender = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        verbose_name=_("Пол"),
        help_text=_("Укажите ваш пол"),
        default=MALE,
    )
    start_datetime = models.DateTimeField(auto_now_add=True)
    last_datetime = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(
        verbose_name=_("Широта"),
        help_text=_("Укажите широту"),
        validators=(MinValueValidator(-90.1), MaxValueValidator(90.1)),
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        verbose_name=_("Долгота"),
        help_text=_("Укажите долготу"),
        validators=(MinValueValidator(-180.1), MaxValueValidator(90.1)),
        blank=True,
        null=True,
    )
    friends = models.ManyToManyField(
        "self",
        through="FriendsRelationship",
        verbose_name=_("Друзья"),
        help_text=_("Укажите друзей"),
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.username


class FriendsRelationship(models.Model):
    """Промежуточная/вспомогательная таблица юзер-друзья."""

    current_user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Текущий пользователь"),
        related_name="current_user",
        on_delete=models.CASCADE,
    )
    friend = models.ForeignKey(
        CustomUser,
        verbose_name=_("Друг"),
        related_name="friend",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                name=_("%(app_label)s_%(class)s_unique_relationships"),
                fields=("current_user", "friend"),
            ),
            models.CheckConstraint(
                name=_("%(app_label)s_%(class)s_prevent_self_add"),
                check=~models.Q(current_user=F("friend")),
            ),
        )


class FriendsRequest(models.Model):
    """Таблица запросов в друзья."""

    from_user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Текущий пользователь"),
        related_name="user",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Друг"),
        related_name="new_friend",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                name=_("%(app_label)s_%(class)s_unique_relationships"),
                fields=("from_user", "to_user"),
            ),
            models.CheckConstraint(
                name=_("%(app_label)s_%(class)s_prevent_self_add"),
                check=~models.Q(from_user=F("to_user")),
            ),
        )
