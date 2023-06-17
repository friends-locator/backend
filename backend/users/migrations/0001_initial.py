import colorfield.fields
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),

    ]

    operations = [
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите статус",
                        max_length=50,
                        unique=True,
                        verbose_name="Текст статуса",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статус",
                "verbose_name_plural": "Статусы",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=50,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#FFFFFF",
                        image_field=None,
                        max_length=18,
                        samples=None,
                        unique=True,
                        verbose_name="Цвет",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Ссылка")),
            ],
            options={
                "verbose_name": "Интерес",
                "verbose_name_plural": "Интересы",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите имя",
                        max_length=150,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Введите фамилию",
                        max_length=150,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        help_text="Введите ваш e-mail",
                        max_length=254,
                        verbose_name="E-mail",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="Введите логин",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="Логин",
                    ),
                ),
                (
                    "userpic",
                    models.ImageField(
                        help_text="Выберите изображение",
                        upload_to="uploads/%Y/%m/%d/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpeg", "jpg", "png"]
                            )
                        ],
                        verbose_name="Фото пользователя",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[["Мужской", "Женский"]],
                        help_text="Укажите ваш пол",
                        max_length=50,
                        verbose_name="Пол",
                    ),
                ),
                ("start_datetime", models.DateTimeField(auto_now_add=True)),
                ("last_datetime", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        help_text="Укажите статус",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statuses",
                        to="users.status",
                        verbose_name="Статус",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        help_text="Выберите интересы",
                        related_name="tags",
                        to="users.tag",
                        verbose_name="Интересы",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]