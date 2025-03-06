from rest_framework import serializers

from reviews.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title

    def get_rating(self, obj):
        # Вычисление рэйтинга
        return 0


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', required=True
    )

    class Meta:
        fields = "__all__"
        model = Title
