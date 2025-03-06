from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .v1.views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path('v1/', include(router.urls)),
]
