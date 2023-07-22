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
    "rest_framework_simplejwt",
    "djoser",
    "colorfield",
    "django_filters",
    "drf_yasg",

    # Приложения
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    "social_django",
    "elasticemailbackend"
]

SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'
SOCIAL_AUTH_JSONFIELD_ENABLED = True

AUTHENTICATION_BACKENDS = (
    "social_core.backends.vk.VKOAuth2",
    "social_auth.backends.google.GoogleOAuth2Backend",
    # 'social_auth.backends.contrib.yandex.YandexOAuth2Backend',
    # 'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

MIDDLEWARE = [
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}

# Postgress
# DATABASES = {
#     "default": {
#         "ENGINE": os.getenv("DB_ENGINE", default="django.db.backends.postgresql"),
#         "NAME": os.getenv("DB_NAME", default="postgres"),
#         "USER": os.getenv("POSTGRES_USER", default="postgres"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="adm"),
#         "HOST": os.getenv("DB_HOST", default="db"),
#         "PORT": os.getenv("DB_PORT", default="5432"),
#         "ATOMIC_REQUESTS": True,
#     }
# }

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
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['local_password',]


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

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_VK_OAUTH2_KEY = "51708837"
SOCIAL_AUTH_VK_OAUTH2_SECRET = "yQwp9EVrhiycVlqsE0AQ"
SOCIAL_AUTH_VK_OAUTH2_SCOPE = []
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '131366740845-sc7a64547ckb6bgn27ofgi0lmtjp1u6t.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

EMAIL_BACKEND = "elasticemailbackend.backend.ElasticEmailBackend"

ELASTICEMAIL_API_KEY = os.getenv("ELASTICEMAIL_API_KEY")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", default="friends-locator@yandex.ru")

EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
