import os

from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    default="django-insecure-hnx2%flrjxay-o@nh3#b+b+$c8zfavmnl629_250*y!xudtwn3",
)


DEBUG = True

ALLOWED_HOSTS = (
    "localhost",
    "backend",
    "127.0.0.1",
    "flap.acceleratorpracticum.ru",
    "80.87.106.172",
    "0.0.0.0",
)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Сторонние либы
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "colorfield",
    "django_filters",
    "drf_yasg",

    # Приложения
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    "elasticemailbackend",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    # "http://127.0.0.1:8000",
    # "null",
)


# CORS_ALLOW_HEADERS = default_headers + (
#     'Access-Control-Allow-Origin',
# )

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#         "ATOMIC_REQUESTS": True,
#     }
# }

# Postgress
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="adm"),
        "HOST": os.getenv("DB_HOST", default="db"),
        "PORT": os.getenv("DB_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = "backend_static/"
STATIC_ROOT = BASE_DIR / "backend_static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

DOMAIN = "flap.acceleratorpracticum.ru"
SITE_NAME = "flap.acceleratorpracticum.ru"

DJOSER = {
    "HIDE_USERS": False,
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserCreateSerializer",
        "user": "users.serializers.CustomUserSerializer",
        "current_user": "users.serializers.CustomUserSerializer",
    },
    "ACTIVATION_URL": "api/account-activate/{uid}/{token}/",
    "SEND_ACTIVATION_EMAIL": True,
    # Это нужно будет согласовывать с фронтом: они должны будут принять эту
    # ссылку и вывести экран для ввода нового пароля, который вместе с uid и
    # token улетит на password_reset_confirm
    # "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # "PASSWORD_RESET_CONFIRM_URL": "api/password-change/{uid}/{token}",
    # "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

INTERNAL_IPS = ("127.0.0.1",)
CSRF_TRUSTED_ORIGINS = (
    "http://flap.acceleratorpracticum.ru",
    "https://flap.acceleratorpracticum.ru",
)
AUTH_USER_MODEL = "users.CustomUser"


EMAIL_BACKEND = "elasticemailbackend.backend.ElasticEmailBackend"

ELASTICEMAIL_API_KEY = os.getenv("ELASTICEMAIL_API_KEY")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", default="friends-locator@yandex.ru")

EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
