from rest_framework import serializers

from .models import ShortLink


class ShortLinkSerializer(serializers.ModelSerializer):
    original_link = serializers.URLField(required=True)

    class Meta:
        model = ShortLink
        fields = (
            "id",
            "original_link",
            "short_link",
            "clicks_count",
            "created_at",
        )
        read_only_fields = ("id", "clicks_count", "short_link", "created_at")
