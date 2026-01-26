from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, TourOperator

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_tour_operator', 'is_administrator', 'is_staff')
    list_filter = ('is_tour_operator', 'is_administrator', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'country', 'city')
    search_fields = ('user__email', 'first_name', 'last_name')

@admin.register(TourOperator)
class TourOperatorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'contact_email', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('company_name', 'contact_email', 'user__email')
