"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseAdmin):
    """Define the admin page for the user"""
    ordering = ['id']
    list_display = ['email', 'name', 'last_login',]
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser',)
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # allows to add css classes
            'fields': (
                'email',
                'name',
                'password1',
                'password2',
                'is_staff',
                'is_active',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
