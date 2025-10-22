from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from django.core.management.base import BaseCommand, CommandError

from places.models import Place


def _infer_city(address: str | None, default_city: str | None) -> str:
    if address:
        text = address.strip()
        parts = [p.strip() for p in text.split(",") if p and p.strip()]
        candidates = list(reversed(parts))
        known = {
            "jakarta", "jakarta pusat", "jakarta selatan", "jakarta barat", "jakarta timur", "jakarta utara",
            "bogor", "depok", "bekasi", "tangerang", "tangerang selatan",
        }
        for p in candidates:
            low = p.lower()
            for k in known:
                if k in low:
                    return p
        if parts:
            return parts[-1]
    return default_city or "Unknown"


def _map_facility_type(types_field: str | None) -> str:
    if not types_field:
        return Place.FacilityType.GYM
    text = types_field.lower()

    if "swimming_pool" in text or "swim" in text:
        return Place.FacilityType.SWIM

    court_signals = [
        "soccer", "futsal", "basketball", "badminton", "tennis", "volleyball", "table_tennis", "ring",
        "stadium", "pitch",
    ]
    if any(sig in text for sig in court_signals):
        return Place.FacilityType.COURT

    studio_signals = ["yoga", "zumba", "pilates", "aerobics", "barre", "hiit", "dance", "studio"]
    if any(sig in text for sig in studio_signals):
        return Place.FacilityType.STUDIO

    if "outdoor" in text or "track" in text:
        return Place.FacilityType.OUTDOOR

    wellness_signals = ["sauna", "spa", "recovery", "breathwork", "cold_plunge", "light_therapy"]
    if any(sig in text for sig in wellness_signals):
        return Place.FacilityType.WELLNESS

    if "fitness_centre" in text or "fitness" in text:
        return Place.FacilityType.GYM

    return Place.FacilityType.GYM


def _parse_sports_and_tags(types_field: str | None) -> list[str]:
    if not types_field:
        return []
    items: list[str] = []
    for chunk in types_field.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("sport:"):
            sports = chunk.split(":", 1)[1]
            for s in sports.split(";"):
                s = s.strip().replace("_", " ")
                if s:
                    items.append(s)
        elif chunk.startswith("leisure:"):
            val = chunk.split(":", 1)[1].strip().replace("_", " ")
            if val:
                items.append(val)
        else:
            tok = chunk.replace("_", " ")
            if tok:
                items.append(tok)
    seen = set()
    out: list[str] = []
    for i in items:
        low = i.lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(i)
    return out


class Command(BaseCommand):
    help = "Import places from jabodetabek_sports_with_wiki_images.csv into Place"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default="jabodetabek_sports_with_wiki_images.csv",
            help="Path to CSV file (defaults to jabodetabek_sports_with_wiki_images.csv)",
        )
        parser.add_argument(
            "--default-city",
            default=None,
            help="Default city if not derivable from address",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing records matched by name (case-insensitive)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing Place records before import",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv"]).expanduser()
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        default_city = options.get("default_city")
        do_update: bool = bool(options.get("update"))
        do_clear: bool = bool(options.get("clear"))

        created = 0
        updated = 0
        skipped = 0

        if do_clear:
            Place.objects.all().delete()

        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Required columns; 'city' is optional (we'll infer from address if missing).
            expected = {
                "name",
                "address",
                "lat",
                "lng",
                "types",
                "osm_link",
                "image_link",
                "osm_type",
                "osm_id",
            }
            missing = expected - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"CSV missing columns: {', '.join(sorted(missing))}")

            for row in reader:
                name = (row.get("name") or "").strip()
                if not name:
                    skipped += 1
                    continue
                address = (row.get("address") or "").strip()
                city_raw = (row.get("city") or "").strip()
                city = city_raw or _infer_city(address, default_city)
                types_field = (row.get("types") or "").strip()
                image_link = (row.get("image_link") or "").strip()
                lat_raw = (row.get("lat") or "").strip()
                lng_raw = (row.get("lng") or "").strip()
                try:
                    lat = float(lat_raw) if lat_raw else None
                except ValueError:
                    lat = None
                try:
                    lng = float(lng_raw) if lng_raw else None
                except ValueError:
                    lng = None

                facility_type = _map_facility_type(types_field)
                amenities = _parse_sports_and_tags(types_field)
                tags = ",".join(amenities[:8])

                qs = Place.objects.filter(name__iexact=name)
                instance: Place | None = qs.first()

                payload = dict(
                    address=address or "",
                    city=city,
                    facility_type=facility_type,
                    amenities=amenities,
                    tags=tags,
                    hero_image=image_link,
                    gallery=[image_link] if image_link else [],
                    latitude=lat,
                    longitude=lng,
                    is_active=True,
                )

                if instance:
                    if do_update:
                        for k, v in payload.items():
                            setattr(instance, k, v)
                        instance.save()
                        updated += 1
                    else:
                        skipped += 1
                else:
                    instance = Place(name=name, **payload)
                    instance.save()
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created} updated={updated} skipped={skipped} from {csv_path.name}"
            )
        )
