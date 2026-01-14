from rest_framework import serializers
from .models import Booking, Payment, Review
from tourism.models import TouristSite
from accounts.models import User


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'tourist_site', 'booking_date', 'number_of_visitors',
                  'total_price', 'status', 'special_requests', 'created_at', 'updated_at')
        read_only_fields = ('user', 'status', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'booking', 'amount', 'payment_method', 'transaction_id',
                  'status', 'payment_date')
        read_only_fields = ('status', 'payment_date')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'tourist_site', 'rating', 'comment', 'is_verified',
                  'created_at', 'updated_at')
        read_only_fields = ('user', 'is_verified', 'created_at', 'updated_at')