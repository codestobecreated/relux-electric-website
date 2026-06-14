import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from business.models import FranchiseInquiry

class Command(BaseCommand):
    help = 'Seeds franchise inquiries from FranchiseEnquiry.csv'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'FranchiseEnquiry.csv')
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at: {csv_file_path}"))
            return

        self.stdout.write(f"Reading CSV from {csv_file_path}...")
        
        count = 0
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row_id = int(row['id'])
                    franchise_type = row.get('franchise_type', '')
                    name = row.get('name', '')
                    email = row.get('email', '')
                    phone = row.get('phone', '')
                    state = row.get('state', '')
                    city = row.get('city', '')
                    business_profile = row.get('business_profile', '')
                    investment_range = row.get('investment_range', '')
                    message = row.get('message', '')
                    created_at_str = row.get('created_at', '')

                    obj, created = FranchiseInquiry.objects.update_or_create(
                        id=row_id,
                        defaults={
                            'franchise_model': franchise_type,
                            'full_name': name,
                            'email': email,
                            'phone': phone,
                            'state': state,
                            'city': city,
                            'business_profile': business_profile,
                            'investment_capacity': investment_range,
                            'message': message,
                        }
                    )

                    if created_at_str:
                        dt = parse_datetime(created_at_str)
                        if dt:
                            if settings.USE_TZ:
                                try:
                                    dt_aware = make_aware(dt)
                                except Exception:
                                    dt_aware = dt
                            else:
                                dt_aware = dt
                            # Bypass auto_now_add=True
                            FranchiseInquiry.objects.filter(id=obj.id).update(created_at=dt_aware)

                    count += 1
                    if count % 100 == 0:
                        self.stdout.write(f"Processed {count} rows...")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row.get('id')}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} franchise inquiries!"))
