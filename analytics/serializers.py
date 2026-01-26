from rest_framework import serializers
from .models import UserAnalytics, AttractionAnalytics, TourAnalytics, BookingAnalytics, SystemAnalytics

class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = ['total_bookings', 'total_spent', 'favorite_categories', 'last_active']
        read_only_fields = ['total_bookings', 'total_spent', 'favorite_categories', 'last_active']

class AttractionAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionAnalytics
        fields = ['total_views', 'total_bookings', 'average_rating', 'total_reviews', 'peak_season']
        read_only_fields = ['total_views', 'total_bookings', 'average_rating', 'total_reviews', 'peak_season']

class TourAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAnalytics
        fields = ['total_bookings', 'total_revenue', 'average_rating', 'total_reviews', 'completion_rate']
        read_only_fields = ['total_bookings', 'total_revenue', 'average_rating', 'total_reviews', 'completion_rate']

class BookingAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingAnalytics
        fields = ['date', 'total_bookings', 'total_revenue', 'bookings_by_tour', 'bookings_by_user_type']
        read_only_fields = ['date', 'total_bookings', 'total_revenue', 'bookings_by_tour', 'bookings_by_user_type']

class SystemAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAnalytics
        fields = ['date', 'total_users', 'total_attractions', 'total_tours', 'total_bookings', 'total_revenue', 'top_destinations']
        read_only_fields = ['date', 'total_users', 'total_attractions', 'total_tours', 'total_bookings', 'total_revenue', 'top_destinations']