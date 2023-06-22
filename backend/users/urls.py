from django.contrib import admin
from django.urls import path

app_name = "users"

urlpatterns = [
    path("...", admin.site.urls),
]
