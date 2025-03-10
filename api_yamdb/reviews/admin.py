from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import ADMIN_PAGE_TEXT_LIMIT


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category', 'get_genres')
    filter_horizontal = ('genre',)
    search_fields = ('name', 'year')
    list_filter = ('category', 'genre')
    list_editable = ('category',)
    empty_value_display = '-пусто-'

    @admin.display(description='Жанры')
    def get_genres(self, obj):
        return [genre.name for genre in obj.genre.all()]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Genre)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'review_text_view',
        'score',
        'pub_date'
    )
    search_fields = ('text', 'title__name')
    list_filter = ('pub_date', 'author')

    @admin.display(description='Текст отзыва')
    def review_text_view(self, obj):
        return f'{obj.text[:ADMIN_PAGE_TEXT_LIMIT]}''...'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'comment_text_view', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')

    @admin.display(description='Текст комментария')
    def comment_text_view(self, obj):
        return f'{obj.text[:ADMIN_PAGE_TEXT_LIMIT]}''...'
