from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ActivityLog, User, WishlistItem


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": ("display_name", "role", "avatar"),
            },
        ),
    )
    list_display = ("username", "email", "display_name", "role", "is_staff")
    list_filter = ("role", "is_staff")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("user__username", "user__email")


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "place", "trainer", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "place__name", "trainer__name")
