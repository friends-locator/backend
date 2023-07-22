from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("users/", include("users.urls", namespace="users")),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
]
