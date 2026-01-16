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
        request = self.context.get('request')
        
        # Allow status updates only for superusers
        if 'status' in validated_data:
            if request and request.user.is_superuser:
                instance.status = validated_data['status']
            else:
                # Remove status from validated_data if user is not superuser
                validated_data.pop('status', None)
        
        # Update other fields if they are provided
        for field in ['booking_date', 'number_of_visitors', 'total_price', 'special_requests', 'tourist_site']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
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