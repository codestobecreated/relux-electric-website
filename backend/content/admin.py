from django.contrib import admin
from .models import Blog, Video, Event, BlogCategory, BlogTag, EventImage, Article, VideoHeroSlide

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'author')
    list_filter = ('is_published', 'category')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    search_fields = ('name',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url', 'created_at')
    search_fields = ('title',)

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('date',)
    inlines = [EventImageInline]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'category')

@admin.register(VideoHeroSlide)
class VideoHeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'highlight_text', 'subtitle', 'order', 'is_active')
    search_fields = ('title', 'highlight_text', 'subtitle')
    list_filter = ('is_active',)




