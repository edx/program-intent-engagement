""" Admin configuration for core models. """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from program_intent_engagement.apps.core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Admin configuration for the custom User model. """
    list_display = ('username', 'lms_user_id', 'email', 'full_name', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'lms_user_id', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
