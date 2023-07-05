from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import TagViewSet
from users.views import CustomUserViewSet

app_name = "api"


schema_view = get_schema_view(
   openapi.Info(
      title="\"Where are my friends?\" API",
      default_version='v1',
      description="Документация приложения backend проекта \"Где друзья?\"",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("users", CustomUserViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
]


# Отдельный набор путей для документации
urlpatterns += [
    path('v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path('v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
