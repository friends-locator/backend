from django.db import router
from django.urls import include, path

from users.views import CustomUserViewSet

app_name = "api"

router.register("users", CustomUserViewSet)
include(router.urls)
path("v1/", include("djoser.urls"))
path("v1/", include("djoser.urls.jwt")),

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
