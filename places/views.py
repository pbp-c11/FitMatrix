from __future__ import annotations

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


def place_list(request: HttpRequest) -> HttpResponse:
    """Backward-compatible shim pointing to the dedicated search app."""
    return search_results_view(request)


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
    return render(
        request,
        "places/detail.html",
        {
            "place": place,
            "recommended": recommended_places(limit=6),
            "nearby": nearby,
            "is_favorite": is_favorite,
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
