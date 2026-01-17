from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ShortLinkRedirectAPIView, ShortLinkViewSet

app_name = "links"

router = SimpleRouter()

router.register("links", ShortLinkViewSet, basename="links")

urlpatterns = [
    path(
        "get_short/<str:short_link>/",
        ShortLinkRedirectAPIView.as_view(),
        name="short-link-redirect",
    ),
    path("", include(router.urls)),
]
