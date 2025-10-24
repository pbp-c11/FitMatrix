from __future__ import annotations

from django import forms

from .models import SessionSlot


class SessionSlotForm(forms.ModelForm):
    class Meta:
        model = SessionSlot
        fields = ("trainer", "place", "start", "end", "capacity", "is_active")
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start")
        end = cleaned.get("end")
        if start and end and end <= start:
            self.add_error("end", "End time must be after start time.")
        return cleaned
