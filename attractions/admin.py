from django.contrib import admin
from .models import AttractionCategory, Attraction, AttractionImage, AttractionReview

@admin.register(AttractionCategory)
class AttractionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

class AttractionImageInline(admin.TabularInline):
    model = AttractionImage
    extra = 1

class AttractionReviewInline(admin.TabularInline):
    model = AttractionReview
    extra = 1

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'country', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'country')
    search_fields = ('name', 'city', 'country')
    inlines = [AttractionImageInline, AttractionReviewInline]

@admin.register(AttractionImage)
class AttractionImageAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'caption', 'is_primary', 'created_at')
    list_filter = ('is_primary',)

@admin.register(AttractionReview)
class AttractionReviewAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'user', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified')
