from django.db import models
from accounts.models import User
from attractions.models import Attraction
from tours.models import Tour
from bookings.models import Booking
from django.utils.translation import gettext_lazy as _

class UserAnalytics(models.Model):
    """Analytics data for user behavior"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    total_bookings = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    favorite_categories = models.JSONField(default=list)  # Store list of category IDs
    last_active = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.user.email}"

class AttractionAnalytics(models.Model):
    """Analytics data for attractions"""
    attraction = models.OneToOneField(Attraction, on_delete=models.CASCADE, related_name='analytics')
    total_views = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    total_reviews = models.PositiveIntegerField(default=0)
    peak_season = models.CharField(max_length=20, blank=True)  # Store peak season info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.attraction.name}"

class TourAnalytics(models.Model):
    """Analytics data for tours"""
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE, related_name='analytics')
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    total_reviews = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.tour.title}"

class BookingAnalytics(models.Model):
    """Analytics data for bookings"""
    date = models.DateField()
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bookings_by_tour = models.JSONField(default=dict)  # Store tour_id: count mapping
    bookings_by_user_type = models.JSONField(default=dict)  # Store user_type: count mapping
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('date',)

    def __str__(self):
        return f"Booking Analytics for {self.date}"

class SystemAnalytics(models.Model):
    """System-wide analytics data"""
    date = models.DateField()
    total_users = models.PositiveIntegerField(default=0)
    total_attractions = models.PositiveIntegerField(default=0)
    total_tours = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    top_destinations = models.JSONField(default=list)  # Store list of top attraction IDs
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('date',)

    def __str__(self):
        return f"System Analytics for {self.date}"
