from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet
)
from users.views import GetToken, UserSignUp, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('token/', GetToken.as_view(), name='token')
]

v1_urls = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls))
]

urlpatterns = [
    path('v1/', include(v1_urls)),
]
