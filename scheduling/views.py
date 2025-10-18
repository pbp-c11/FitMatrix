from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import SessionSlot


@login_required
def upcoming_sessions(request):
    slots = SessionSlot.objects.select_related("trainer", "place").order_by("start")
    return render(request, "scheduling/sessions.html", {"slots": slots})
