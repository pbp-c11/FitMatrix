from __future__ import annotations

import time
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from places.models import Place
from reviews.models import Review
from scheduling.forms import SessionSlotForm
from scheduling.models import Booking, SessionSlot, Trainer

from .forms import AccessiblePasswordChangeForm, LoginForm, ProfileForm, RegisterForm
from .models import ActivityLog, User, WishlistItem

THROTTLE_LIMIT = 5
THROTTLE_TIMEOUT = 600  # seconds
THROTTLE_DELAY = 2


def is_admin(user: User) -> bool:
    return user.is_authenticated and user.is_admin


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        ActivityLog.objects.create(user=user, type=ActivityLog.Types.LOGIN)
        messages.success(request, "Welcome to FitMatrix! Your account is ready.")
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


def _throttle_key(identifier: str, request: HttpRequest) -> str:
    client_id = request.META.get("REMOTE_ADDR", "unknown")
    return f"login_attempts:{identifier.lower()}:{client_id}"


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = LoginForm(request.POST or None)
    throttle_identifier = request.POST.get("identifier", "")
    key = _throttle_key(throttle_identifier, request)
    attempts = cache.get(key, 0)
    if request.method == "POST":
        if attempts >= THROTTLE_LIMIT:
            time.sleep(THROTTLE_DELAY)
            form.add_error(None, "Invalid credentials.")
        elif form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                cache.delete(key)
                ActivityLog.objects.create(user=user, type=ActivityLog.Types.LOGIN)
                messages.success(request, "You are logged in.")
                return redirect("accounts:profile")
        else:
            cache.set(key, attempts + 1, THROTTLE_TIMEOUT)
            if attempts + 1 >= THROTTLE_LIMIT:
                time.sleep(THROTTLE_DELAY)
    return render(request, "accounts/login.html", {"form": form, "throttled": attempts >= THROTTLE_LIMIT})


@require_POST
@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    ActivityLog.objects.create(user=request.user, type=ActivityLog.Types.LOGOUT)
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    now = timezone.now()
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("slot__trainer", "slot__place")
        .order_by("-slot__start")
    )
    current_booking = bookings.filter(
        slot__start__lte=now,
        slot__end__gte=now,
        status=Booking.Status.BOOKED,
    ).first()
    past_bookings = bookings.filter(slot__end__lt=now)
    activity_page = Paginator(
        ActivityLog.objects.filter(user=request.user),
        10,
    ).get_page(request.GET.get("page"))
    wishlist_qs = (
        WishlistItem.objects.filter(user=request.user)
        .select_related("place", "trainer")
        .order_by("-created_at")
    )
    wishlist_page = Paginator(wishlist_qs, 12).get_page(request.GET.get("wishlist_page"))
    reviews = Review.objects.filter(user=request.user).select_related("trainer")
    profile_form = ProfileForm(instance=request.user)
    password_form = AccessiblePasswordChangeForm(user=request.user)
    context = {
        "current_booking": current_booking,
        "past_bookings": past_bookings,
        "activity_page": activity_page,
        "wishlist_page": wishlist_page,
        "reviews": reviews,
        "profile_form": profile_form,
        "password_form": password_form,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        ActivityLog.objects.create(user=user, type=ActivityLog.Types.PROFILE_UPDATED)
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile_edit.html", {"form": form})


class DashboardPasswordChangeView(PasswordChangeView):
    form_class = AccessiblePasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form: AccessiblePasswordChangeForm) -> HttpResponse:
        response = super().form_valid(form)
        ActivityLog.objects.create(
            user=self.request.user,
            type=ActivityLog.Types.PASSWORD_CHANGED,
        )
        messages.success(self.request, "Password updated successfully.")
        return response


@login_required
@require_GET
def activity_history_view(request: HttpRequest) -> HttpResponse:
    logs = ActivityLog.objects.filter(user=request.user)
    page_obj = Paginator(logs, 20).get_page(request.GET.get("page"))
    return render(request, "accounts/activity_history.html", {"page_obj": page_obj})


@login_required
@require_GET
def wishlist_view(request: HttpRequest) -> HttpResponse:
    items = (
        WishlistItem.objects.filter(user=request.user)
        .select_related("place", "trainer")
        .order_by("-created_at")
    )
    page_obj = Paginator(items, 12).get_page(request.GET.get("page"))
    return render(request, "accounts/wishlist.html", {"page_obj": page_obj})


@login_required
@require_POST
def wishlist_toggle_view(request: HttpRequest, kind: str, pk: int) -> HttpResponse:
    if kind not in {"place", "trainer"}:
        return JsonResponse({"error": "Invalid kind"}, status=400)
    model = Place if kind == "place" else Trainer
    target = get_object_or_404(model, pk=pk)
    filters: dict[str, object] = {"user": request.user}
    if kind == "place":
        filters["place"] = target
    else:
        filters["trainer"] = target
    item = WishlistItem.objects.filter(**filters).first()
    if item:
        item.delete()
        ActivityLog.objects.create(
            user=request.user,
            type=ActivityLog.Types.WISHLIST_REMOVED,
            meta={"kind": kind, "id": pk},
        )
        state = "removed"
    else:
        item = WishlistItem(user=request.user)
        if kind == "place":
            item.place = target
        else:
            item.trainer = target
        item.save()
        ActivityLog.objects.create(
            user=request.user,
            type=ActivityLog.Types.WISHLIST_ADDED,
            meta={"kind": kind, "id": pk},
        )
        state = "added"
    return JsonResponse({"status": state})


@user_passes_test(is_admin)
def admin_console_view(request: HttpRequest) -> HttpResponse:
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    upcoming_slots = SessionSlot.objects.filter(start__gte=timezone.now()).count()
    return render(
        request,
        "accounts/admin/console.html",
        {
            "total_users": total_users,
            "total_bookings": total_bookings,
            "upcoming_slots": upcoming_slots,
        },
    )


@user_passes_test(is_admin)
def admin_slots_list(request: HttpRequest) -> HttpResponse:
    slots = SessionSlot.objects.select_related("trainer", "place").order_by("start")
    return render(request, "accounts/admin/slots_list.html", {"slots": slots})


@user_passes_test(is_admin)
def admin_slot_create(request: HttpRequest) -> HttpResponse:
    form = SessionSlotForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Session slot created.")
        return redirect("accounts:admin-slots")
    return render(request, "accounts/admin/slot_form.html", {"form": form})


@user_passes_test(is_admin)
def admin_slot_edit(request: HttpRequest, pk: int) -> HttpResponse:
    slot = get_object_or_404(SessionSlot, pk=pk)
    form = SessionSlotForm(request.POST or None, instance=slot)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Session slot updated.")
        return redirect("accounts:admin-slots")
    return render(request, "accounts/admin/slot_form.html", {"form": form, "slot": slot})


@user_passes_test(is_admin)
@require_POST
def admin_slot_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    slot = get_object_or_404(SessionSlot, pk=pk)
    slot.is_active = not slot.is_active
    slot.save(update_fields=["is_active"])
    messages.info(request, "Slot status updated.")
    return redirect("accounts:admin-slots")


@user_passes_test(is_admin)
def admin_bookings_list(request: HttpRequest) -> HttpResponse:
    bookings = (
        Booking.objects.select_related("user", "slot__trainer", "slot__place")
        .order_by("-created_at")
    )
    return render(request, "accounts/admin/bookings_list.html", {"bookings": bookings})


@user_passes_test(is_admin)
@require_POST
def admin_booking_cancel(request: HttpRequest, pk: int) -> HttpResponse:
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == Booking.Status.CANCELLED:
        messages.warning(request, "Booking already cancelled.")
    else:
        booking.cancel(by_admin=True)
        messages.success(request, "Booking cancelled.")
    return redirect("accounts:admin-bookings")


@user_passes_test(is_admin)
def admin_reviews_list(request: HttpRequest) -> HttpResponse:
    reviews = Review.objects.select_related("trainer", "user", "booking")
    return render(request, "accounts/admin/reviews_list.html", {"reviews": reviews})


@user_passes_test(is_admin)
@require_POST
def admin_review_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    review = get_object_or_404(Review, pk=pk)
    review.is_visible = not review.is_visible
    review.save(update_fields=["is_visible"])
    messages.info(request, "Review visibility updated.")
    return redirect("accounts:admin-reviews")
