from rest_framework.viewsets import ReadOnlyModelViewSet
from api.serializers import TagSerializer
from users.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
