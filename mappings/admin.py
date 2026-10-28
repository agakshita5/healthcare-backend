from django.contrib import admin

from .models import Mapping


@admin.register(Mapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "created_at"]
    autocomplete_fields = ["patient", "doctor"]
