from django.contrib import admin
from .models import UserAnalytics, AttractionAnalytics, TourAnalytics, BookingAnalytics, SystemAnalytics

@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_bookings', 'total_spent', 'last_active')
    search_fields = ('user__email',)

@admin.register(AttractionAnalytics)
class AttractionAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'total_views', 'total_bookings', 'average_rating', 'total_reviews')
    search_fields = ('attraction__name',)

@admin.register(TourAnalytics)
class TourAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('tour', 'total_bookings', 'total_revenue', 'average_rating', 'total_reviews', 'completion_rate')
    search_fields = ('tour__title',)

@admin.register(BookingAnalytics)
class BookingAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_bookings', 'total_revenue')
    list_filter = ('date',)

@admin.register(SystemAnalytics)
class SystemAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'total_attractions', 'total_tours', 'total_bookings', 'total_revenue')
    list_filter = ('date',)
