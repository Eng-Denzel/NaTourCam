from django.contrib import admin
from .models import Tour, TourImage, TourItinerary, TourAvailability

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

class TourItineraryInline(admin.TabularInline):
    model = TourItinerary
    extra = 1

class TourAvailabilityInline(admin.TabularInline):
    model = TourAvailability
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'tour_operator', 'duration_days', 'price', 'currency', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'difficulty_level', 'currency', 'tour_operator')
    search_fields = ('title', 'tour_operator__company_name')
    inlines = [TourImageInline, TourItineraryInline, TourAvailabilityInline]

@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'caption', 'is_primary', 'created_at')

@admin.register(TourItinerary)
class TourItineraryAdmin(admin.ModelAdmin):
    list_display = ('tour', 'day_number', 'title', 'location')

@admin.register(TourAvailability)
class TourAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('tour', 'date', 'spots_available', 'is_available')
    list_filter = ('is_available', 'date')
