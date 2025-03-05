from rest_framework import viewsets, permissions
from .models import Title
from .serializers import ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    BasePermission
)


class IsAuthorOrReadOnly(BasePermission):
    """
    Права доступа: автор отзыва, модератор или администратор.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_object(self):
        queryset = self.get_queryset()
        review_id = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=review_id)
        return obj
