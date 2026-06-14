import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from business.models import Location

locations = Location.objects.all()
print(f"Total locations in DB: {locations.count()}")
for loc in locations:
    print(f"ID: {loc.id}, Name: {loc.name}, Active: {loc.is_active}, Lat: {loc.latitude}, Long: {loc.longitude}, City: {loc.city}")
