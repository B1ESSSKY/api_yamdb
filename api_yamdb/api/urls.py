from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import GetToken, UserSignUp, UserViewSet
from .v1.views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('token/', GetToken.as_view(), name='token')
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
