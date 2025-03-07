from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminModeratorAuthorOrReadOnly
from reviews.models import Title, Category, Genre, Review
from rest_framework.exceptions import ValidationError
from .serializers import (
    TitleReadSerializer,
    TitleWriteSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class GenreCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = PageNumberPagination

    def get_object(self):
        slug = self.kwargs.get("pk")
        obj = get_object_or_404(self.get_queryset(), slug=slug)
        return obj


class CategoryViewSet(GenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly]

    def get_queryset(self):
        """Получение queryset для отзывов конкретного произведения."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохранение отзыва с автором и произведением."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            raise ValidationError(
                "Вы уже оставили отзыв к этому произведению."
            )

        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly]

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
