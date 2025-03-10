from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import ValidationError
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

    def get_object(self):
        slug = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), slug=slug)
        return obj


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

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminOrReadOnly,)

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

    def get_queryset(self):
        """Получение queryset для отзывов конкретного произведения."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение отзыва с автором и произведением."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists():
            raise ValidationError(
                'Вы уже оставили отзыв к этому произведению.'
            )

        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (
        IsAdminModeratorAuthorOrReadOnly, IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        """Получение queryset для комментариев конкретного отзыва."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохранение комментария с автором и отзывом."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
