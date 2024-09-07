from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


@admin.register(User)
class UserAdminConfig(BaseUserAdmin):
    ordering = ['-date_joined']
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'phone_number']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']

    fieldsets = (
        ("Personal Information", {'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_staff',
                'is_superuser',
                'is_active')
        }),
    )
    readonly_fields = ['date_joined', 'last_login']
