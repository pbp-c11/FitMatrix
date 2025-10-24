from django.shortcuts import render

from places.models import Place
from places.services import (
    facility_filters,
    newest_places,
    recommended_places,
    spotlight_places,
)


def home_view(request):
    summary = {
        "place_count": Place.objects.active().count(),
        "studio_count": Place.objects.active().filter(facility_type=Place.FacilityType.STUDIO).count(),
        "trainer_count": Place.objects.active().filter(facility_type__in=[Place.FacilityType.GYM, Place.FacilityType.STUDIO]).count(),
    }
    context = {
        "hero_places": recommended_places(limit=3),
        "spotlight_places": spotlight_places(limit=3),
        "newest_places": newest_places(limit=6),
        "facility_filters": facility_filters(),
        "summary": summary,
    }
    return render(request, "home.html", context)
