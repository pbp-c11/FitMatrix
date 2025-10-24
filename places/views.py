from __future__ import annotations

<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from search.views import results_view as search_results_view

from accounts.models import WishlistItem

from .forms import ReviewForm
from .models import Place, Review
from .services import recommended_places
from django.template.loader import render_to_string


def place_list(request: HttpRequest) -> HttpResponse:
    """Backward-compatible shim pointing to the dedicated search app."""
    return search_results_view(request)

@require_POST
@login_required
def place_review_create(request, slug: str):
    """Submit review via AJAX dan balas partial list terbaru."""
    mgr = getattr(Place.objects, "active", None)
    place = get_object_or_404(mgr() if callable(mgr) else Place.objects.all(), slug=slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.create(
            place=place,
            user=request.user,
            rating=int(form.cleaned_data["rating"]),
            body=form.cleaned_data.get("body", "").strip(),
        )

        reviews = _sorted_reviews_qs(place, sort="created_at", direction="desc")
        html = render_to_string(
            "places/_reviews.html",
            {
                "place": place,
                "reviews": reviews,
                "active_sort": "created_at",
                "active_dir": "desc",
            },
            request=request,
        )
        return JsonResponse({"ok": True, "html": html, "count": reviews.count()})

    # kirim error kalau form gak valid
    errors_html = render_to_string(
        "places/_review_form_errors.html",
        {"form": form},
        request=request,
    )
    return JsonResponse({"ok": False, "errors_html": errors_html}, status=400)


@require_GET
def place_detail(request, slug: str):
    place = get_object_or_404(Place.objects.active(), slug=slug)
    nearby = (
        Place.objects.active()
        .filter(facility_type=place.facility_type)
        .exclude(pk=place.pk)
        .order_by("-highlight_score", "-rating_avg")[:4]
    )
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = WishlistItem.objects.filter(user=request.user, place=place).exists()
    reviews = _sorted_reviews_qs(place, sort="created_at", direction="desc")

    return render(
        request,
        "places/detail.html",
        {
            "place": place,
            "recommended": recommended_places(limit=6),
            "nearby": nearby,
            "is_favorite": is_favorite,
            "reviews": reviews,
        },
    )

ALLOWED_REVIEW_SORTS = {"created_at", "liked", "rating"}

def _sorted_reviews_qs(place, sort, direction):
    qs = Review.objects.filter(place=place).select_related("user")
    if sort == "liked":
        qs = qs.annotate(like_count=Count("likes")); key = "like_count"
    elif sort == "rating":
        key = "rating"
    else:
        key = "created_at"
    return qs.order_by(key if direction == "asc" else f"-{key}", "-id")

@require_GET
def place_reviews_partial(request, slug: str):
    mgr = getattr(Place.objects, "active", None)
    place = get_object_or_404(mgr() if callable(mgr) else Place.objects.all(), slug=slug)

    sort = request.GET.get("sort", "created_at")
    direction = request.GET.get("dir", "desc")
    if sort not in ALLOWED_REVIEW_SORTS or direction not in {"asc","desc"}:
        return HttpResponseBadRequest("Invalid sort parameter")

    reviews = _sorted_reviews_qs(place, sort, direction)

    return render(
        request,
        "places/_reviews.html",
        {
            "place": place,
            "reviews": reviews,
            "active_sort": sort,
            "active_dir": direction,
        },
    )

@require_POST
@login_required
def place_review_create(request, slug: str):
    """Submit review via AJAX; balas partial list terbaru."""
    mgr = getattr(Place.objects, "active", None)
    place = get_object_or_404(mgr() if callable(mgr) else Place.objects.all(), slug=slug)

    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.create(
            place=place,
            user=request.user,
            rating=int(form.cleaned_data["rating"]),
            body=form.cleaned_data.get("body", "").strip(),
        )

        # setelah simpan, render ulang daftar review (default: terbaru duluan)
        reviews = _sorted_reviews_qs(place, sort="created_at", direction="desc")
        html = render(request, "places/_reviews.html", {
            "place": place,
            "reviews": reviews,
            "active_sort": "created_at",
            "active_dir": "desc",
        }).content.decode("utf-8")
        return JsonResponse({"ok": True, "html": html})

    # kirim error form
    errors_html = render(request, "places/_review_form_errors.html", {"form": form}).content.decode("utf-8")
    return JsonResponse({"ok": False, "errors_html": errors_html}, status=400)
=======
from typing import Iterable

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from accounts.models import WishlistItem

from .models import Place
from .services import (
    facility_filters,
    price_filter_options,
    recommended_places,
    search_places,
    spotlight_places,
)


def _request_amenities(request) -> list[str]:
    amenities: Iterable[str] = request.GET.getlist("amenities")
    if not amenities:
        raw = request.GET.get("amenities")
        if raw:
            amenities = [item.strip() for item in raw.split(",")]
    return [item for item in amenities if item]


@require_GET
def place_list(request):
    query = request.GET.get("q", "").strip()
    facility_type = request.GET.get("type") or request.GET.get("facility_type")
    city = request.GET.get("city", "").strip()
    price_key = request.GET.get("price")
    amenities = _request_amenities(request)
    sort = request.GET.get("sort")

    places = search_places(
        query=query or None,
        facility_type=facility_type,
        city=city or None,
        price_key=price_key,
        amenities=amenities or None,
    )
    if sort == "newest":
        places = places.order_by("-created_at")
    elif sort == "rating":
        places = places.order_by("-rating_avg", "-likes")

    context = {
        "places": places,
        "query": query,
        "facility_filters": facility_filters(),
        "selected_type": (facility_type or "ALL").upper(),
        "selected_price": price_key or "",
        "price_filters": price_filter_options(),
        "city": city,
        "selected_amenities": amenities,
        "spotlights": spotlight_places(limit=3),
        "sort": sort or "",
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("places/_cards.html", context, request=request)
        return JsonResponse({"html": html, "count": places.count()})

    return render(request, "places/list.html", context)


def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    nearby = Place.objects.exclude(pk=place.pk)[:3]
    recommended = Place.objects.all()[:3]

    # 💡 Tambahan baru: cek apakah tempat ini ada di wishlist user
    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = WishlistItem.objects.filter(user=request.user, place=place).exists()

    context = {
        "place": place,
        "nearby": nearby,
        "recommended": recommended,
        "is_in_wishlist": is_in_wishlist,
    }
    return render(request, "places/detail.html", context)
>>>>>>> origin/kanayradeeva010
