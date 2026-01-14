from django.contrib import admin
from .models import Booking, Payment, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tourist_site', 'booking_date', 'number_of_visitors', 'total_price', 'status')
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = ('user__email', 'user__username', 'tourist_site__name')
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount', 'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('transaction_id', 'booking__id')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tourist_site', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('user__email', 'tourist_site__name', 'comment')
