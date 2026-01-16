import uuid

from django.db import models


# Create your models here.
class ShortLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    short_link = models.CharField(
        max_length=12,
        unique=True,
        db_index=True,
        verbose_name="Короткая ссылка",
    )

    original_link = models.URLField(max_length=2048, verbose_name="Оригинальная ссылка")

    is_active = models.BooleanField(default=True, verbose_name="Активна")

    clicks_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество переходов"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.short_link} - {self.original_link}"
