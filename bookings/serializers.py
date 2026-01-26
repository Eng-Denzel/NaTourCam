from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
from .models import Booking, BookingParticipant, Payment

class BookingParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingParticipant
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 
                  'passport_number', 'nationality']
        read_only_fields = ['id']

class BookingSerializer(serializers.ModelSerializer):
    participants_details = BookingParticipantSerializer(many=True, read_only=True)
    tour_title = serializers.CharField(source='tour.title', read_only=True)
    tour_operator = serializers.CharField(source='tour.tour_operator.company_name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'tour', 'tour_title', 'tour_operator', 'tour_availability',
                  'participants', 'total_price', 'currency', 'status', 'special_requests',
                  'emergency_contact_name', 'emergency_contact_phone', 'participants_details',
                  'booking_date', 'confirmation_date', 'cancellation_date']
        read_only_fields = ['id', 'user', 'status', 'booking_date', 'confirmation_date', 'cancellation_date']

class BookingCreateSerializer(serializers.ModelSerializer):
    participants_details = BookingParticipantSerializer(many=True)
    
    class Meta:
        model = Booking
        fields = ['tour', 'tour_availability', 'participants', 'special_requests',
                  'emergency_contact_name', 'emergency_contact_phone', 'participants_details']
    
    def validate(self, data):
        # Check if tour availability has enough spots
        tour_availability = data['tour_availability']
        participants = data['participants']
        
        if tour_availability.spots_available < participants:
            raise serializers.ValidationError(
                f"Not enough spots available. Only {tour_availability.spots_available} spots left."
            )
        
        # Check if tour availability date matches tour dates
        tour = data['tour']
        availability_date = tour_availability.date
        
        if not (tour.start_date <= availability_date <= tour.end_date):
            raise serializers.ValidationError(
                "Selected date is not within the tour's valid date range."
            )
        
        return data
    
    def create(self, validated_data):
        participants_data = validated_data.pop('participants_details')
        validated_data['user'] = self.context['request'].user
        validated_data['total_price'] = validated_data['tour'].price * validated_data['participants']
        validated_data['currency'] = validated_data['tour'].currency
        
        booking = Booking.objects.create(**validated_data)
        
        # Create participant details
        for participant_data in participants_data:
            BookingParticipant.objects.create(booking=booking, **participant_data)
        
        # Update tour availability
        tour_availability = booking.tour_availability
        tour_availability.spots_available -= booking.participants
        tour_availability.save()
        
        return booking

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'currency', 'payment_method',
                  'transaction_id', 'status', 'payment_date']
        read_only_fields = ['id', 'status', 'payment_date']

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking', 'payment_method']
    
    def validate_booking(self, value):
        # Ensure the booking belongs to the requesting user
        request = self.context.get('request')
        if request and request.user != value.user:
            raise serializers.ValidationError("You can only make payments for your own bookings.")
        
        # Ensure the booking is in pending status
        if value.status != 'pending':
            raise serializers.ValidationError("This booking cannot be paid for.")
        
        return value
    
    def create(self, validated_data):
        booking = validated_data['booking']
        validated_data['amount'] = booking.total_price
        validated_data['currency'] = booking.currency
        validated_data['transaction_id'] = f"txn_{booking.id}_{int(datetime.now().timestamp())}"
        validated_data['status'] = 'completed'  # In a real app, this would be pending until payment is processed
        validated_data['payment_date'] = timezone.now()
        
        payment = Payment.objects.create(**validated_data)
        
        # Update booking status
        booking.status = 'confirmed'
        booking.confirmation_date = timezone.now()
        booking.save()
        
        return payment