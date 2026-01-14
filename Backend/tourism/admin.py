from django.contrib import admin
from .models import Region, TouristSite, SiteImage, BilingualContent


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(TouristSite)
class TouristSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_active', 'created_at')
    list_filter = ('region', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'address')
    ordering = ('name',)


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('site', 'caption', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('site__name', 'caption')


@admin.register(BilingualContent)
class BilingualContentAdmin(admin.ModelAdmin):
    list_display = ('site', 'language', 'title', 'created_at')
    list_filter = ('language', 'created_at')
    search_fields = ('site__name', 'title', 'description')
