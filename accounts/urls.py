from __future__ import annotations

from django.urls import path
from . import views

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
    wishlist_collections_view,
    create_collection_view,
    delete_collection_view,
    wishlist_collection_detail_view,
    get_user_collections, 
    add_to_collection_view
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
    path("wishlist/collections/", wishlist_collections_view, name="wishlist-collections"),
    path("create-collection/", create_collection_view, name="create-collection"),
    path("wishlist/collections/<int:pk>/delete/", delete_collection_view, name="delete-collection"),
    path("wishlist/collections/<int:pk>/", views.wishlist_collection_detail_view, name="wishlist-collection-detail"),
    path("collections/list/", views.get_user_collections, name="get-user-collections"),
    path("collections/add/", views.add_to_collection_view, name="add-to-collection"),
    path("collections/item/<int:pk>/delete/", views.delete_collection_item_view, name="delete-collection-item"),


]
