import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from business.models import Location, LocationReview

def seed_sample_data():
    # Clear existing locations to have a clean slate of 4 locations to test
    print("Clearing existing locations...")
    Location.objects.all().delete()

    samples = [
        {
            "name": "Relux Electric Experience Center - Guindy",
            "address": "16/8, PRV Towers, GST Road, Guindy, Chennai, Tamil Nadu 600032",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "latitude": 13.007671,
            "longitude": 80.207513,
            "status": "active",
            "facilities": "Restroom, Parking, Seating Area, Cafe",
            "charger_connector": "AC Type 2",
            "charger_power": "7.2 kW",
            "charger_count": 2,
            "google_map_url": "https://www.google.com/maps/dir/?api=1&destination=13.007671,80.207513",
            "reviews": [
                {"name": "Anand Kumar", "rating": 5, "date_str": "2 days ago", "comment": "Excellent experience, chargers are working fine. Staff is very helpful!"},
                {"name": "Priya R", "rating": 4, "date_str": "1 week ago", "comment": "Great location, near the highway. Cafe is handy."}
            ]
        },
        {
            "name": "Relux Charging Station - Indiranagar",
            "address": "100 Feet Rd, Indiranagar, Bengaluru, Karnataka 560038",
            "city": "Bengaluru",
            "state": "Karnataka",
            "country": "India",
            "latitude": 12.971891,
            "longitude": 77.641151,
            "status": "active",
            "facilities": "Restroom, Cafe, Wifi, Parking",
            "charger_connector": "CCS2 (DC Fast)",
            "charger_power": "60 kW",
            "charger_count": 4,
            "google_map_url": "https://www.google.com/maps/dir/?api=1&destination=12.971891,77.641151",
            "reviews": [
                {"name": "Rahul Verma", "rating": 5, "date_str": "3 days ago", "comment": "Super fast charging! Got from 20% to 80% in just 35 mins."},
                {"name": "Siddharth S", "rating": 5, "date_str": "5 days ago", "comment": "Clean restrooms and reliable power supply."}
            ]
        },
        {
            "name": "Relux Super Hub - Somajiguda",
            "address": "Khairatabad Rd, Somajiguda, Hyderabad, Telangana 500004",
            "city": "Hyderabad",
            "state": "Telangana",
            "country": "India",
            "latitude": 17.416260,
            "longitude": 78.457912,
            "status": "active",
            "facilities": "Restroom, Food Court, Parking",
            "charger_connector": "CCS2 (DC Fast)",
            "charger_power": "120 kW",
            "charger_count": 6,
            "google_map_url": "https://www.google.com/maps/dir/?api=1&destination=17.416260,78.457912",
            "reviews": [
                {"name": "Vikram Dev", "rating": 5, "date_str": "1 day ago", "comment": "Amazing 120kW speed, best in class!"}
            ]
        },
        {
            "name": "Relux Charging Station - Mulund",
            "address": "Devidayal Rd, Mulund West, Mumbai, Maharashtra 400080",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "latitude": 19.1726,
            "longitude": 72.9565,
            "status": "active",
            "facilities": "Restroom, Parking, Cafe",
            "charger_connector": "AC Type 2",
            "charger_power": "22 kW",
            "charger_count": 2,
            "google_map_url": "https://www.google.com/maps/dir/?api=1&destination=19.1726,72.9565",
            "reviews": [
                {"name": "Amit Shah", "rating": 4, "date_str": "4 days ago", "comment": "Convenient location and decent charging speed."}
            ]
        }
    ]

    for item in samples:
        reviews_data = item.pop("reviews")
        loc = Location.objects.create(**item)
        print(f"Created location: {loc.name} in {loc.city}")
        for r in reviews_data:
            LocationReview.objects.create(location=loc, **r)
            print(f"  Added review by {r['name']}")

    print("\nSuccessfully added 4 sample locations with reviews!")

if __name__ == "__main__":
    seed_sample_data()
