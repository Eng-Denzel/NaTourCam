from rest_framework import serializers
from .models import Booking, Payment, Review
from tourism.models import TouristSite
from accounts.models import User


class BookingSerializer(serializers.ModelSerializer):
    tourist_site_name = serializers.CharField(source='tourist_site.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'user', 'tourist_site', 'tourist_site_name', 'booking_date', 
                  'number_of_visitors', 'total_price', 'status', 'special_requests', 
                  'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def update(self, instance, validated_data):
        # Allow status updates only for superusers
        request = self.context.get('request')
        if request and request.user.is_superuser:
            instance.status = validated_data.get('status', instance.status)
        
        # Update other fields
        instance.booking_date = validated_data.get('booking_date', instance.booking_date)
        instance.number_of_visitors = validated_data.get('number_of_visitors', instance.number_of_visitors)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.special_requests = validated_data.get('special_requests', instance.special_requests)
        instance.save()
        return instance


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