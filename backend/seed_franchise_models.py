import os
import sys
import django
import urllib.request

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.models import FranchiseModelCard


def download_image(url, folder, filename):
    os.makedirs(f"media/{folder}", exist_ok=True)
    filepath = f"media/{folder}/{filename}"
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  Downloaded: {filepath}")
        except Exception as e:
            print(f"  Error downloading {url}: {e}")
            return ""
    return f"{folder}/{filename}"


def seed_franchise_models():
    print("\n========================================")
    print("  Seeding Franchise Model Cards...")
    print("========================================\n")

    franchise_models_data = [
        {
            "title": "MINI 30KW",
            "capacity": "30 KW",
            "space": "200 - 400 SQ.FT",
            "desc": "Perfect entry-level charging station for petrol pumps, retail outlets, and small commercial spaces. Low footprint, high impact.",
            "image_url": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?q=80&w=2072&auto=format&fit=crop",
            "filename": "franchise_mini_30kw.jpg",
            "order": 1,
        },
        {
            "title": "STD 60KW",
            "capacity": "60 KW",
            "space": "400 - 800 SQ.FT",
            "desc": "The most popular franchise model. Ideal for parking lots, malls, and corporate campuses. Balanced investment with strong ROI.",
            "image_url": "https://images.unsplash.com/photo-1616618819034-2b89f7c4ddc1?q=80&w=2072&auto=format&fit=crop",
            "filename": "franchise_std_60kw.jpg",
            "order": 2,
        },
        {
            "title": "PRO 120KW",
            "capacity": "120 KW",
            "space": "800 - 1500 SQ.FT",
            "desc": "High-performance charging hub for highways, fleet operators, and premium commercial zones. Built for maximum throughput.",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?q=80&w=2072&auto=format&fit=crop",
            "filename": "franchise_pro_120kw.jpg",
            "order": 3,
        },
        {
            "title": "HYPER 240KW",
            "capacity": "240 KW",
            "space": "1500 - 3000 SQ.FT",
            "desc": "Ultra-fast charging infrastructure for dedicated EV hubs, highway corridors, and large fleet charging depots.",
            "image_url": "https://images.unsplash.com/photo-1540575861501-7cf05a4b125a?q=80&w=2070&auto=format&fit=crop",
            "filename": "franchise_hyper_240kw.jpg",
            "order": 4,
        },
        {
            "title": "MEGA HUB",
            "capacity": "500 KW+",
            "space": "3000+ SQ.FT",
            "desc": "Full-scale Relux charging park with multiple bays, solar canopy, lounge, and café. The flagship franchise experience.",
            "image_url": "https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?q=80&w=2069&auto=format&fit=crop",
            "filename": "franchise_mega_hub.jpg",
            "order": 5,
        },
    ]

    for item in franchise_models_data:
        img_path = download_image(item["image_url"], "franchise_models", item["filename"])

        obj, created = FranchiseModelCard.objects.get_or_create(
            title=item["title"],
            defaults={
                "capacity": item["capacity"],
                "space": item["space"],
                "desc": item["desc"],
                "image": img_path,
                "order": item["order"],
                "is_active": True,
            }
        )

        if created:
            print(f"  [CREATED] {obj.title} — {obj.capacity}")
        else:
            # Update existing record
            obj.capacity = item["capacity"]
            obj.space = item["space"]
            obj.desc = item["desc"]
            obj.order = item["order"]
            obj.is_active = True
            if img_path:
                obj.image = img_path
            obj.save()
            print(f"  [UPDATED] {obj.title} — {obj.capacity}")

    total = FranchiseModelCard.objects.filter(is_active=True).count()
    print(f"\n  Total active franchise model cards in DB: {total}")
    print("\n  Franchise Model Cards seeding COMPLETE!")


if __name__ == "__main__":
    seed_franchise_models()
