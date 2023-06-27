from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TagViewSet
from users.views import CustomUserViewSet

app_name = "api"

router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("users", CustomUserViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),    path("v1/", include("djoser.urls")),    path("v1/", include("djoser.urls.jwt")),
]
