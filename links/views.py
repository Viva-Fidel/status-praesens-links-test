from django.core.cache import cache
from django.db.models import F
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortLink
from .serializers import ShortLinkSerializer
from .services import check_link_in_redis, url_to_base62


# Create your views here.
class ShortLinkViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
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


class ShortLinkRedirectAPIView(APIView):
    @extend_schema(
        summary="Получение оригинальной ссылки по короткой",
        description="Возвращает оригинальную ссылку для заданного short_link и увеличивает счетчик кликов",
        parameters=[
            OpenApiExample(
                name="Short link",
                value="abc123",
                description="Короткий идентификатор ссылки",
            )
        ],
        responses={
            200: OpenApiResponse(
                response={"original_link": "https://example.com"},
                description="Оригинальная ссылка успешно найдена",
            ),
            404: OpenApiResponse(
                response={"detail": "Short link not found"},
                description="Ссылка с таким short_link не найдена",
            ),
        },
    )
    def get(self, request, short_link: str):
        redis_key = check_link_in_redis(short_link)
        original_link = cache.get(redis_key)

        if original_link:
            ShortLink.objects.filter(short_link=short_link).update(
                clicks_count=F("clicks_count") + 1
            )
            return Response(
                {
                    "original_link": original_link,
                },
                status=status.HTTP_200_OK,
            )

        try:
            obj = ShortLink.objects.get(short_link=short_link)
        except ShortLink.DoesNotExist:
            return Response(
                {"detail": "Short link not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cache.set(redis_key, obj.original_link)

        ShortLink.objects.filter(pk=obj.pk).update(clicks_count=F("clicks_count") + 1)

        return Response(
            {
                "original_link": obj.original_link,
            },
            status=status.HTTP_200_OK,
        )
