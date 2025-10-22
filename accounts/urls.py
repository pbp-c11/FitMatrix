from __future__ import annotations

from django.urls import path

from .views import (
    DashboardPasswordChangeView,
    activity_history_view,
    admin_booking_cancel,
    admin_bookings_list,
    admin_console_view,
    admin_review_toggle,
    admin_reviews_list,
    admin_slot_create,
    admin_slot_edit,
    admin_slot_toggle,
    admin_slots_list,
    login_view,
    logout_view,
    profile_edit_view,
    profile_view,
    register_view,
    wishlist_toggle_view,
    wishlist_view,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile-edit"),
    path("password/", DashboardPasswordChangeView.as_view(), name="password"),
    path("history/", activity_history_view, name="history"),
    path("wishlist/", wishlist_view, name="wishlist"),
    path("wishlist/toggle/<str:kind>/<int:pk>/", wishlist_toggle_view, name="wishlist-toggle"),
    path("admin/console/", admin_console_view, name="admin-console"),
    path("admin/slots/", admin_slots_list, name="admin-slots"),
    path("admin/slots/new/", admin_slot_create, name="admin-slot-create"),
    path("admin/slots/<int:pk>/edit/", admin_slot_edit, name="admin-slot-edit"),
    path("admin/slots/<int:pk>/toggle/", admin_slot_toggle, name="admin-slot-toggle"),
    path("admin/bookings/", admin_bookings_list, name="admin-bookings"),
    path("admin/bookings/<int:pk>/cancel/", admin_booking_cancel, name="admin-booking-cancel"),
    path("admin/reviews/", admin_reviews_list, name="admin-reviews"),
    path("admin/reviews/<int:pk>/toggle/", admin_review_toggle, name="admin-review-toggle"),
]
