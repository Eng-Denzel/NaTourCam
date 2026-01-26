from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class AttractionCategory(models.Model):
    """Categories for tourist attractions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For icon representation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Attraction Categories"

    def __str__(self):
        return self.name

class Attraction(models.Model):
    """Model for tourist attractions"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(AttractionCategory, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_attractions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AttractionImage(models.Model):
    """Images for attractions"""
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='attractions/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attraction.name} - {self.caption}"

class AttractionReview(models.Model):
    """Reviews for attractions"""
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)  # Verified visitor
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('attraction', 'user')

    def __str__(self):
        return f"{self.attraction.name} - {self.user.email}"
