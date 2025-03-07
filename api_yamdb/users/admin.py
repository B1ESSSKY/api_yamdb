from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'role', 'bio'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    empty_value_display = '-пусто-'
