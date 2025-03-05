from rest_framework import serializers
from .models import Review, Title
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date', 'title']
        read_only_fields = ['author', 'pub_date', 'title']


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
