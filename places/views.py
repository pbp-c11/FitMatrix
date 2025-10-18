from __future__ import annotations

from django.shortcuts import render

from .models import Place


def place_list(request):
    places = Place.objects.filter(is_active=True)
    return render(request, "places/list.html", {"places": places})
