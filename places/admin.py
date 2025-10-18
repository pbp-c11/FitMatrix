from django.contrib import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "is_free", "price", "is_active")
    list_filter = ("city", "is_free", "is_active")
    search_fields = ("name", "city")
