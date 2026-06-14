from django.contrib import admin

from .models import HomeAboutImage, NetworkStat, CompanyCoreTab, FranchiseModelCard

@admin.register(HomeAboutImage)
class HomeAboutImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'is_active', 'order')
    list_editable = ('is_active', 'order')

@admin.register(NetworkStat)
class NetworkStatAdmin(admin.ModelAdmin):
    list_display = ('id', 'locations', 'charge_points', 'now_building')
    list_editable = ('locations', 'charge_points', 'now_building')

@admin.register(CompanyCoreTab)
class CompanyCoreTabAdmin(admin.ModelAdmin):
    list_display = ('tab_id', 'label', 'order')
    list_editable = ('label', 'order')
    search_fields = ('tab_id', 'label')

@admin.register(FranchiseModelCard)
class FranchiseModelCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'capacity', 'space', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'capacity')
