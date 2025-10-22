from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class PlaceQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def recommendable(self):
        return self.active().filter(highlight_score__gte=1)

    def by_type(self, facility_type: str | None):
        if not facility_type or facility_type.lower() in {"", "all"}:
            return self
        return self.filter(facility_type=facility_type)

    def search(self, query: str | None):
        if not query:
            return self
        return self.filter(
            models.Q(name__icontains=query)
            | models.Q(city__icontains=query)
            | models.Q(address__icontains=query)
            | models.Q(tagline__icontains=query)
            | models.Q(summary__icontains=query)
            | models.Q(tags__icontains=query),
        )


class Place(models.Model):
    class FacilityType(models.TextChoices):
        GYM = "GYM", "Gym"
        STUDIO = "STUDIO", "Studio"
        SWIM = "SWIM", "Swimming Pool"
        OUTDOOR = "OUTDOOR", "Outdoor"
        WELLNESS = "WELLNESS", "Wellness"
        COURT = "COURT", "Court"

    name = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=160,
        unique=True,
        blank=True,
        null=True,
        help_text="Used for public URLs.",
    )
    tagline = models.CharField(max_length=160, blank=True)
    summary = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    facility_type = models.CharField(
        max_length=32,
        choices=FacilityType.choices,
        default=FacilityType.GYM,
    )
    amenities = models.JSONField(default=list, blank=True)
    highlight_score = models.PositiveSmallIntegerField(
        default=0,
        help_text="Higher scores surface first in recommendations.",
    )
    accent_color = models.CharField(
        max_length=9,
        blank=True,
        help_text="CSS color shorthand (e.g. #7FEB45).",
    )
    hero_image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Relative static path or absolute URL for hero visuals.",
    )
    gallery = models.JSONField(default=list, blank=True)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rating_avg = models.FloatField(default=0)
    likes = models.PositiveIntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    opening_hours = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PlaceQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["facility_type", "-highlight_score"]),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "place"
            slug_candidate = base
            counter = 1
            Model = type(self)
            while Model.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                counter += 1
                slug_candidate = f"{base}-{counter}"
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def price_display(self) -> str:
        if self.is_free:
            return "Free access"
        if self.price is None:
            return "Pricing on request"
        amount = f"{self.price:,.0f}".replace(",", ".")
        return f"Rp {amount}"

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse("places:detail", kwargs={"slug": self.slug})

    def primary_color(self) -> str:
        return self.accent_color or "#03B863"

    def amenities_list(self) -> list[str]:
        value = self.amenities or []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    def gallery_list(self) -> list[str]:
        value = self.gallery or []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    def map_embed_url(self, *, zoom: int = 16) -> str:
        if self.latitude is None or self.longitude is None:
            return ""
        # Tight bbox around the marker for a closer default zoom.
        delta = 0.005  # ~500–700m window depending on latitude
        south = self.latitude - delta
        north = self.latitude + delta
        west = self.longitude - delta
        east = self.longitude + delta
        bbox = f"{west:.6f},{south:.6f},{east:.6f},{north:.6f}"
        return (
            "https://www.openstreetmap.org/export/embed.html?"
            f"bbox={bbox}&layer=mapnik&marker={self.latitude:.6f}%2C{self.longitude:.6f}"
        )

    def google_maps_url(self) -> str:
        if self.latitude is None or self.longitude is None:
            return ""
        return f"https://www.google.com/maps?q={self.latitude:.6f},{self.longitude:.6f}"
