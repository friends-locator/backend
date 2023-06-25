from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import TagViewSet

app_name = "api"

router = DefaultRouter()
router.register("tags", TagViewSet)

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
]
