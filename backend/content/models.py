from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blogs/')
    category = models.ForeignKey('BlogCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs')
    author = models.CharField(max_length=100)
    read_time = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 5 min read")
    tag = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. TECHNOLOGY")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='videos/')
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=50, default='YouTube')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    time = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 10 Am To 10 Pm")
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    @property
    def count(self):
        return self.blogs.filter(is_published=True).count()

    def __str__(self):
        return f"{self.name} ({self.count})"

class BlogTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.title} ({self.id})"

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/')
    category = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Charging Hubs")
    author = models.CharField(max_length=100, default='Relux Team')
    read_time = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 5 min read")
    media_link = models.URLField(blank=True, null=True, help_text="e.g. https://timesofindia.indiatimes.com/...")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class VideoHeroSlide(models.Model):
    title = models.CharField(max_length=255, help_text="e.g. FUTURE IS")
    highlight_text = models.CharField(max_length=100, help_text="e.g. NOW.")
    subtitle = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Innovation")
    tagline = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 2 Years ago")
    views_count = models.CharField(max_length=50, default="12K Views")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hero_slides/')
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} {self.highlight_text}"





