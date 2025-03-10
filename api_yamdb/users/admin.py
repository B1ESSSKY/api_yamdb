from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'role', 'bio'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {
            'fields': (
                'first_name', 'last_name', 'email', 'bio')
        }),
        ('Роль', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Личные данные', {
            'fields': (
                'first_name', 'last_name', 'email', 'bio')
        }),
        ('Роль', {'fields': ('role',)}),
    )
