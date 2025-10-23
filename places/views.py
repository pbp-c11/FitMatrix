from __future__ import annotations

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
