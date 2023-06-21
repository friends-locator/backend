from django.contrib import admin
from django.urls import include, path

app_name = "users"

urlpatterns = [
    path("...", admin.site.urls),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
]
