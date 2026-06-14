from django.db import models

class Location(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    facilities = models.TextField(blank=True, null=True, help_text="Comma-separated list, e.g. Restroom, Cafe, Seating Area")
    charger_connector = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. CCS2, AC Type 2")
    charger_power = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 120 kW, 60 kW")
    charger_count = models.IntegerField(default=1)
    google_map_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def avg_rating(self):
        active_reviews = self.reviews.filter(is_active=True)
        if active_reviews.exists():
            return round(sum(r.rating for r in active_reviews) / active_reviews.count(), 1)
        return 4.8

    @property
    def total_reviews(self):
        active_reviews = self.reviews.filter(is_active=True)
        return active_reviews.count() if active_reviews.exists() else 124

    def __str__(self):
        return f"{self.name} - {self.city}"

class LocationReview(models.Model):
    location = models.ForeignKey(Location, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    date_str = models.CharField(max_length=50, help_text="e.g. 2 days ago")
    comment = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.location.name}"


ENQUIRY_STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('responded', 'Responded'),
    ('called_closed', 'Called & Closed'),
]

class FranchiseInquiry(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    investment_capacity = models.CharField(max_length=100)
    franchise_model = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., MINI 30KW, STD 60 KW")
    business_profile = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., ENTREPRENEUR, REAL ESTATE OWNER")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Admin tracking fields
    status = models.CharField(max_length=20, choices=ENQUIRY_STATUS_CHOICES, default='new')
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    response_note = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Franchise: {self.full_name} ({self.city})"

class ZeroInvestmentPartner(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location_offered = models.TextField(blank=True, null=True) # preserve compatibility
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    land_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 2400")
    land_unit = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., SQ.FT, ACRES")
    electricity_connection = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., YES, NO")
    land_photo = models.FileField(upload_to='zero_land_photos/', blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Admin tracking fields
    status = models.CharField(max_length=20, choices=ENQUIRY_STATUS_CHOICES, default='new')
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    response_note = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"ZeroInvest: {self.full_name} ({self.city if self.city else ''})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Admin tracking fields
    status = models.CharField(max_length=20, choices=ENQUIRY_STATUS_CHOICES, default='new')
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    response_note = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Message from {self.name}: {self.subject if self.subject else 'No Subject'}"

