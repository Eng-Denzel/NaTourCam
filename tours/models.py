from django.db import models
from accounts.models import User, TourOperator
from attractions.models import Attraction
from django.utils.translation import gettext_lazy as _

class Tour(models.Model):
    """Model for tour packages"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    tour_operator = models.ForeignKey(TourOperator, on_delete=models.CASCADE, related_name='tours')
    attractions = models.ManyToManyField(Attraction, related_name='tours', blank=True)
    duration_days = models.PositiveIntegerField()
    max_participants = models.PositiveIntegerField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('moderate', 'Moderate'),
            ('challenging', 'Challenging'),
            ('difficult', 'Difficult')
        ],
        default='moderate'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    start_date = models.DateField()
    end_date = models.DateField()
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    includes = models.TextField(help_text="What's included in the tour")
    excludes = models.TextField(help_text="What's not included in the tour", blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tours')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TourImage(models.Model):
    """Images for tours"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tour.title} - {self.caption}"

class TourItinerary(models.Model):
    """Daily itinerary for tours"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='itinerary')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    accommodation = models.CharField(max_length=200, blank=True)
    meals = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"{self.tour.title} - Day {self.day_number}: {self.title}"

class TourAvailability(models.Model):
    """Availability dates for tours"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    spots_available = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tour', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.tour.title} - {self.date}"
