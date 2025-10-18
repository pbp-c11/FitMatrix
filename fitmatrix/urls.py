from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views
from .views import home_view

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("accounts/", include("accounts.urls")),
    path("places/", include("places.urls")),
    path("scheduling/", include("scheduling.urls")),
    path("reviews/", include("reviews.urls")),
    path("admin/console/", account_views.admin_console_view, name="admin-console"),
    path("admin/slots/", account_views.admin_slots_list, name="admin-slots"),
    path("admin/slots/new/", account_views.admin_slot_create, name="admin-slot-create"),
    path("admin/slots/<int:pk>/edit/", account_views.admin_slot_edit, name="admin-slot-edit"),
    path("admin/slots/<int:pk>/toggle/", account_views.admin_slot_toggle, name="admin-slot-toggle"),
    path("admin/bookings/", account_views.admin_bookings_list, name="admin-bookings"),
    path("admin/bookings/<int:pk>/cancel/", account_views.admin_booking_cancel, name="admin-booking-cancel"),
    path("admin/reviews/", account_views.admin_reviews_list, name="admin-reviews"),
    path("admin/reviews/<int:pk>/toggle/", account_views.admin_review_toggle, name="admin-review-toggle"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
