"""
Management command to seed charging locations from CSV into the database.
Usage: python manage.py seed_locations --csv locations.csv
"""
import csv
import os
from django.core.management.base import BaseCommand
from business.models import Location


def build_google_maps_url(lat, lng):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"


class Command(BaseCommand):
    help = "Seed charging locations from the CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            default=None,
            help="Path to the CSV file",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing locations before seeding",
        )

    def handle(self, *args, **options):
        # Resolve CSV path
        csv_path = options.get("csv")
        if not csv_path:
            # Look in the project backend folder or project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            possible_paths = [
                os.path.join(base_dir, "locations.csv"),
                os.path.join(os.path.dirname(base_dir), "locations.csv"),
                "locations.csv",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    csv_path = path
                    break

        if not csv_path or not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found. Pass --csv <path>"))
            return

        self.stdout.write(f"Reading CSV: {csv_path}")

        if options.get("clear"):
            count = Location.objects.count()
            Location.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {count} existing locations."))

        created = 0
        skipped = 0
        updated = 0

        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("Name") or "").strip()
                address = (row.get("Address") or "").strip()
                city = (row.get("City") or "").strip()
                state = (row.get("State") or "").strip()
                country = (row.get("Country") or "India").strip()
                zip_code = (row.get("Zip Code") or "").strip()
                lat_str = (row.get("Latitude") or "").strip()
                lng_str = (row.get("Longitude") or "").strip()
                status = (row.get("Status") or "active").strip().lower()
                facilities = (row.get("Facilities") or "").strip()
                charger_connector = (row.get("Charger Connector") or "").strip()
                charger_power = (row.get("Charger Power") or "").strip()
                charger_count_str = (row.get("Charger Count") or "1").strip()
                is_active_str = (row.get("Is Active") or "Yes").strip()

                if not name or not lat_str or not lng_str:
                    self.stdout.write(self.style.WARNING(f"  Skipping row (missing name or lat/lng): {row}"))
                    skipped += 1
                    continue

                try:
                    lat = float(lat_str)
                    lng = float(lng_str)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"  Skipping {name!r}: bad lat/lng values"))
                    skipped += 1
                    continue

                try:
                    charger_count = int(charger_count_str)
                except ValueError:
                    charger_count = 1

                is_active = is_active_str.lower() in ("yes", "true", "1")
                gmaps_url = build_google_maps_url(lat, lng)

                defaults = dict(
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    zip_code=zip_code,
                    latitude=lat,
                    longitude=lng,
                    google_map_url=gmaps_url,
                    status=status if status in ("active", "inactive") else "active",
                    is_active=is_active,
                    charger_connector=charger_connector,
                    charger_power=charger_power,
                    charger_count=charger_count,
                    facilities=facilities,
                )

                obj, was_created = Location.objects.update_or_create(
                    name=name,
                    defaults=defaults,
                )

                if was_created:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"  [+] Created: {name} ({city}, {state})"))
                else:
                    updated += 1
                    self.stdout.write(f"  [~] Updated: {name} ({city}, {state})")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done! Created: {created}  |  Updated: {updated}  |  Skipped: {skipped}"
        ))
