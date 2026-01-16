from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ShortLinkViewSet

app_name = "links"

router = SimpleRouter()

router.register("links", ShortLinkViewSet, basename="links")

urlpatterns = [
    path("", include(router.urls)),
]
