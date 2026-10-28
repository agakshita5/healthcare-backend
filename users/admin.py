from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# default UserAdmin expects username/first_name/last_name, so list our fields
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "name", "is_staff"]
    search_fields = ["email", "name"]
    fieldsets = [
        (None, {"fields": ["email", "name", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_superuser"]}),
    ]
    add_fieldsets = [
        (None, {"fields": ["email", "name", "password1", "password2"]}),
    ]
