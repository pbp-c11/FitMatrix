from __future__ import annotations

<<<<<<< HEAD
import json
=======
>>>>>>> origin/kanayradeeva010
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
<<<<<<< HEAD
from django.views.decorators.csrf import csrf_exempt

from reviews.models import Review
from scheduling.forms import SessionSlotForm, TrainerForm
from scheduling.models import Booking, SessionSlot, Trainer
from places.models import Place
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import WishlistCollection

from .forms import (
    AccessiblePasswordChangeForm,
    AdminPlaceForm,
    AdminUserCreationForm,
    LoginForm,
    ProfileForm,
    RegisterForm,
)
from .models import ActivityLog, CollectionItem, User, WishlistCollection, WishlistItem
=======
from django.contrib.auth.decorators import login_required
from .models import CollectionItem
from .models import WishlistCollection
from places.models import Place
from reviews.models import Review
from scheduling.forms import SessionSlotForm
from django.views.decorators.http import require_GET
from scheduling.models import Booking, SessionSlot, Trainer

from .forms import AccessiblePasswordChangeForm, LoginForm, ProfileForm, RegisterForm
from .models import ActivityLog, User, WishlistItem
from django.views.decorators.csrf import csrf_exempt
import json

>>>>>>> origin/kanayradeeva010

THROTTLE_LIMIT = 5
THROTTLE_TIMEOUT = 600  # seconds
THROTTLE_DELAY = 2


<<<<<<< HEAD
def is_admin(user: User) -> bool:
    return user.is_authenticated and user.is_admin


@login_required
def wishlist_page(request):
    collections = (
        WishlistCollection.objects.filter(user=request.user)
        .filter(user=request.user)
        .prefetch_related("items__place") # biar ngambil semua tempat
        .order_by("name")
    )
    return render(
        request,
        "accounts/wishlist_page.html",
        {"collections": collections},
    )

@login_required
def delete_collection_view(request, pk):
    """AJAX-friendly delete endpoint"""
    if request.method == "POST":
        collection = get_object_or_404(WishlistCollection, pk=pk, user=request.user)
        collection.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def delete_collection_item_view(request, pk):
    if request.method == "POST":
        item = get_object_or_404(WishlistItem, pk=pk, collection__user=request.user)
        item.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def wishlist_collection_detail(request, pk):
    collection = get_object_or_404(WishlistCollection, pk=pk, user=request.user)
    items = collection.items.select_related("place")
=======
@login_required
def wishlist_collection_detail_view(request, pk):
    collection = get_object_or_404(WishlistCollection, pk=pk, user=request.user)
    items = CollectionItem.objects.filter(collection=collection).select_related("place")

>>>>>>> origin/kanayradeeva010
    return render(request, "accounts/wishlist_collection_detail.html", {
        "collection": collection,
        "items": items,
    })


<<<<<<< HEAD
=======
@login_required
@require_GET
def get_user_collections(request: HttpRequest) -> JsonResponse:
    collections = WishlistCollection.objects.filter(user=request.user).values("id", "name")
    return JsonResponse({"collections": list(collections)})


@login_required
@require_POST
def delete_collection_view(request: HttpRequest, pk: int) -> JsonResponse:
    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return JsonResponse({"status": "invalid_request"}, status=400)

    collection = get_object_or_404(WishlistCollection, pk=pk, user=request.user)
    collection.delete()
    return JsonResponse({"status": "deleted"})



@login_required
@csrf_exempt
@require_POST
def create_collection_view(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    name = data.get("name")
    desc = data.get("description", "")
    place_id = data.get("place_id")

    if not name or not place_id:
        return JsonResponse({"error": "Missing name or place_id"}, status=400)

    collection, created = WishlistCollection.objects.get_or_create(
        user=request.user,
        name=name,
        defaults={"description": desc},
    )

    # Cek kalau item-nya udah ada
    from places.models import Place
    place = Place.objects.get(pk=place_id)
    if CollectionItem.objects.filter(collection=collection, place=place).exists():
        return JsonResponse({"status": "exists"})

    CollectionItem.objects.create(collection=collection, place=place)
    return JsonResponse({"status": "added"})

@login_required
@require_POST
def add_to_collection_view(request: HttpRequest) -> JsonResponse:
    import json
    data = json.loads(request.body)
    collection_id = data.get("collection_id")
    place_id = data.get("place_id")

    if not collection_id or not place_id:
        return JsonResponse({"error": "Missing collection_id or place_id"}, status=400)

    collection = get_object_or_404(WishlistCollection, id=collection_id, user=request.user)
    place = get_object_or_404(Place, pk=place_id)

    if CollectionItem.objects.filter(collection=collection, place=place).exists():
        return JsonResponse({"status": "exists"})

    CollectionItem.objects.create(collection=collection, place=place)
    return JsonResponse({"status": "added", "collection": collection.name})

@login_required
@require_POST
def delete_collection_item_view(request, pk):
    from .models import CollectionItem
    item = get_object_or_404(CollectionItem, pk=pk, collection__user=request.user)
    item.delete()
    return JsonResponse({"status": "deleted"})


@login_required
def wishlist_collections_view(request: HttpRequest) -> HttpResponse:
    # Ambil semua koleksi wishlist milik user yang sedang login
    collections = WishlistCollection.objects.filter(user=request.user).order_by("-created_at")
    
    # Kirim datanya ke template baru, misalnya "accounts/wishlist_collections.html"
    return render(
        request,
        "accounts/wishlist_collections.html",
        {"collections": collections}
    )


def is_admin(user: User) -> bool:
    return user.is_authenticated and user.is_admin


>>>>>>> origin/kanayradeeva010
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


<<<<<<< HEAD
def _require_ajax(request: HttpRequest) -> JsonResponse | None:
    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request."}, status=400)
    return None


def _load_json(request: HttpRequest) -> tuple[dict[str, object], JsonResponse | None]:
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return {}, JsonResponse({"error": "Invalid payload."}, status=400)
    return payload, None


@login_required
@require_GET
def get_user_collections(request: HttpRequest) -> JsonResponse:
    collections = (
        WishlistCollection.objects.filter(user=request.user)
        .order_by("name")
        .values("id", "name")
    )
    return JsonResponse({"collections": list(collections)})


@login_required
@csrf_exempt
@require_POST
def create_collection_view(request):
    import json
    data = json.loads(request.body)
    name = data.get("name")
    description = data.get("description", "")
    place_id = data.get("place_id")

    # Buat / ambil koleksi
    collection, created = WishlistCollection.objects.get_or_create(
        user=request.user,
        name=name,
        defaults={"description": description},
    )

    if place_id:
        place = get_object_or_404(Place, pk=place_id)
        CollectionItem.objects.get_or_create(
            collection=collection,
            place=place
        )

    return JsonResponse({
        "status": "added",
        "collection": {"id": collection.id, "name": collection.name}
    })


@login_required
@csrf_exempt
@require_POST
def add_to_collection_view(request):
    import json
    data = json.loads(request.body)
    collection_id = data.get("collection_id")
    place_id = data.get("place_id")

    collection = get_object_or_404(WishlistCollection, pk=collection_id, user=request.user)
    place = get_object_or_404(Place, pk=place_id)

    CollectionItem.objects.get_or_create(
        collection=collection,
        place=place
    )

    return JsonResponse({
        "status": "added",
        "collection": {"id": collection.id, "name": collection.name}
    })


@login_required
@require_POST
def delete_collection_view(request: HttpRequest, pk: int) -> JsonResponse:
    if (response := _require_ajax(request)) is not None:
        return response
    collection = get_object_or_404(WishlistCollection, pk=pk, user=request.user)
    collection.delete()
    ActivityLog.objects.create(
        user=request.user,
        type=ActivityLog.Types.WISHLIST_REMOVED,
        meta={"collection": pk},
    )
    return JsonResponse({"status": "deleted"})


@login_required
@require_POST
def delete_collection_item_view(request: HttpRequest, pk: int) -> JsonResponse:
    if (response := _require_ajax(request)) is not None:
        return response
    item = get_object_or_404(CollectionItem, pk=pk, collection__user=request.user)
    place_id = item.place_id
    collection_id = item.collection_id
    item.delete()
    ActivityLog.objects.create(
        user=request.user,
        type=ActivityLog.Types.WISHLIST_REMOVED,
        meta={"collection": collection_id, "place": place_id},
    )
    return JsonResponse({"status": "deleted"})


=======
>>>>>>> origin/kanayradeeva010
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


<<<<<<< HEAD
=======
@login_required
@require_GET
def wishlist_view(request: HttpRequest) -> HttpResponse:
    collections = (
        WishlistCollection.objects.filter(user=request.user)
        .prefetch_related("items__place")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/wishlist.html",
        {"collections": collections}
    )


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


>>>>>>> origin/kanayradeeva010
@user_passes_test(is_admin)
def admin_console_view(request: HttpRequest) -> HttpResponse:
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
<<<<<<< HEAD
    total_places = Place.objects.count()
    total_trainers = Trainer.objects.count()
=======
>>>>>>> origin/kanayradeeva010
    upcoming_slots = SessionSlot.objects.filter(start__gte=timezone.now()).count()
    return render(
        request,
        "accounts/admin/console.html",
        {
            "total_users": total_users,
            "total_bookings": total_bookings,
<<<<<<< HEAD
            "total_places": total_places,
            "total_trainers": total_trainers,
=======
>>>>>>> origin/kanayradeeva010
            "upcoming_slots": upcoming_slots,
        },
    )


@user_passes_test(is_admin)
<<<<<<< HEAD
def admin_users_list(request: HttpRequest) -> HttpResponse:
    admins = User.objects.filter(role=User.Roles.ADMIN).order_by("username")
    form = AdminUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        new_admin = form.save()
        messages.success(
            request,
            f"Admin account '{new_admin.username}' created successfully.",
        )
        return redirect("accounts:admin-users")
    return render(
        request,
        "accounts/admin/admins_list.html",
        {"admins": admins, "form": form},
    )


@user_passes_test(is_admin)
def admin_places_list(request: HttpRequest) -> HttpResponse:
    places = Place.objects.order_by("name")
    return render(request, "accounts/admin/places_list.html", {"places": places})


@user_passes_test(is_admin)
def admin_place_create(request: HttpRequest) -> HttpResponse:
    form = AdminPlaceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Place created successfully.")
        return redirect("accounts:admin-places")
    return render(request, "accounts/admin/place_form.html", {"form": form})


@user_passes_test(is_admin)
def admin_place_edit(request: HttpRequest, pk: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=pk)
    form = AdminPlaceForm(request.POST or None, instance=place)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Place updated successfully.")
        return redirect("accounts:admin-places")
    return render(
        request,
        "accounts/admin/place_form.html",
        {"form": form, "place": place},
    )


@user_passes_test(is_admin)
@require_POST
def admin_place_delete(request: HttpRequest, pk: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=pk)
    place.delete()
    messages.info(request, "Place deleted.")
    return redirect("accounts:admin-places")


@user_passes_test(is_admin)
@require_POST
def admin_place_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    place = get_object_or_404(Place, pk=pk)
    place.is_active = not place.is_active
    place.save(update_fields=["is_active"])
    if place.is_active:
        messages.success(request, "Place published.")
    else:
        messages.info(request, "Place hidden from listings.")
    return redirect("accounts:admin-places")


@user_passes_test(is_admin)
def admin_trainers_list(request: HttpRequest) -> HttpResponse:
    trainers = Trainer.objects.order_by("name")
    return render(
        request,
        "accounts/admin/trainers_list.html",
        {"trainers": trainers},
    )


@user_passes_test(is_admin)
def admin_trainer_create(request: HttpRequest) -> HttpResponse:
    form = TrainerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Trainer created successfully.")
        return redirect("accounts:admin-trainers")
    return render(request, "accounts/admin/trainer_form.html", {"form": form})


@user_passes_test(is_admin)
def admin_trainer_edit(request: HttpRequest, pk: int) -> HttpResponse:
    trainer = get_object_or_404(Trainer, pk=pk)
    form = TrainerForm(request.POST or None, instance=trainer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Trainer updated successfully.")
        return redirect("accounts:admin-trainers")
    return render(
        request,
        "accounts/admin/trainer_form.html",
        {"form": form, "trainer": trainer},
    )


@user_passes_test(is_admin)
@require_POST
def admin_trainer_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    trainer = get_object_or_404(Trainer, pk=pk)
    trainer.is_active = not trainer.is_active
    trainer.save(update_fields=["is_active"])
    if trainer.is_active:
        messages.success(request, "Trainer activated.")
    else:
        messages.info(request, "Trainer hidden from public listings.")
    return redirect("accounts:admin-trainers")


@user_passes_test(is_admin)
=======
>>>>>>> origin/kanayradeeva010
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
