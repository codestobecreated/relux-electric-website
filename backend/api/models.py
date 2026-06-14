from django.db import models

# Create your models here.
class HomeAboutImage(models.Model):
    image = models.ImageField(upload_to='home_about/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"About Image {self.id} - {self.alt_text}"

class NetworkStat(models.Model):
    locations = models.IntegerField(default=300)
    charge_points = models.IntegerField(default=500)
    now_building = models.IntegerField(default=120)
    
    class Meta:
        verbose_name = "Network Statistic"
        verbose_name_plural = "Network Statistics"

    def __str__(self):
        return "Network Statistics"

class CompanyCoreTab(models.Model):
    tab_id = models.CharField(max_length=50, unique=True, help_text="e.g., Vision, Mission, Values")
    label = models.CharField(max_length=50)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label

class FranchiseModelCard(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    space = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='franchise_models/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
