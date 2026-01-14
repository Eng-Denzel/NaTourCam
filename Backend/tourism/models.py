from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        db_table = 'regions'


class TouristSite(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tourist_sites')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.TextField(blank=True)
    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tourist_sites'


class SiteImage(models.Model):
    site = models.ForeignKey(TouristSite, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='site_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.site.name} - {self.caption}"
    
    class Meta:
        db_table = 'site_images'


class BilingualContent(models.Model):
    site = models.ForeignKey(TouristSite, on_delete=models.CASCADE, related_name='bilingual_content')
    language = models.CharField(max_length=2, choices=[('en', 'English'), ('fr', 'French')])
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.site.name} - {self.get_language_display()}"
    
    class Meta:
        db_table = 'bilingual_content'
        unique_together = ('site', 'language')
