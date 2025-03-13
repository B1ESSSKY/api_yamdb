from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminOrReadOnly
)
from api.v1.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    TitleReadSerializer, TitleWriteSerializer
)
from reviews.models import Category, Genre, Review, Title


class GenreCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Общий вьюсет для жанров и категорий."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(GenreCategoryViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminOrReadOnly,)
    ordering_fields = ('id', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""

    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (
        IsAdminModeratorAuthorOrReadOnly, IsAuthenticatedOrReadOnly
    )

    def get_title(self):
        """Получаем произведение для отзыва."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        """Получение queryset для отзывов конкретного произведения."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение отзыва с автором и произведением."""
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (
        IsAdminModeratorAuthorOrReadOnly, IsAuthenticatedOrReadOnly
    )

    def get_review(self):
        """Получаем отзыв для комментария."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        """Получение queryset для комментариев конкретного отзыва."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохранение комментария с автором и отзывом."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
