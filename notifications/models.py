from django.db import models
from accounts.models import User
from bookings.models import Booking
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPES = [
        ('booking_confirmation', 'Booking Confirmation'),
        ('booking_cancellation', 'Booking Cancellation'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('payment_failure', 'Payment Failure'),
        ('tour_reminder', 'Tour Reminder'),
        ('tour_update', 'Tour Update'),
        ('system_alert', 'System Alert'),
        ('promotion', 'Promotion'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    related_booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.email} - {self.title}"

class NotificationPreference(models.Model):
    """Model for user notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    booking_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    tour_updates = models.BooleanField(default=True)
    promotions = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user.email}"
