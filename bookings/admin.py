from django.contrib import admin
from .models import Booking, BookingParticipant, Payment

class BookingParticipantInline(admin.TabularInline):
    model = BookingParticipant
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'participants', 'total_price', 'currency', 'status', 'booking_date')
    list_filter = ('status', 'currency', 'booking_date')
    search_fields = ('user__email', 'tour__title')
    inlines = [BookingParticipantInline]

@admin.register(BookingParticipant)
class BookingParticipantAdmin(admin.ModelAdmin):
    list_display = ('booking', 'first_name', 'last_name', 'nationality', 'created_at')
    search_fields = ('first_name', 'last_name', 'nationality')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'currency', 'payment_method', 'transaction_id', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'currency', 'payment_date')
    search_fields = ('transaction_id', 'booking__id')
