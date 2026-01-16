from django.core.cache import cache
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import ShortLink
from .serializers import ShortLinkSerializer
from .services import check_link_in_redis, url_to_base62


# Create your views here.
class ShortLinkViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer

    def create(self, request, *args, **kwargs):
        original_link = request.data.get("original_link")
        short_code = url_to_base62(original_link)
        redis_key = check_link_in_redis(short_code)

        cached_link = cache.get(redis_key)

        if cached_link:
            return Response(
                {
                    "short_link": short_code,
                },
                status=status.HTTP_200_OK,
            )

        obj, _ = ShortLink.objects.get_or_create(
            short_link=short_code,
            defaults={"original_link": original_link},
        )

        cache.set(redis_key, obj.original_link)

        return Response(
            {
                "short_link": obj.short_link,
            },
            status=status.HTTP_201_CREATED,
        )
