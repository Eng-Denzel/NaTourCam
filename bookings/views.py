from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Booking, Payment
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    PaymentSerializer,
    PaymentCreateSerializer
)

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingCancelView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        
        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'This booking cannot be cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update booking status
        booking.status = 'cancelled'
        booking.cancellation_date = timezone.now()
        booking.save()
        
        # Refund payment if it exists
        try:
            payment = booking.payment
            payment.status = 'refunded'
            payment.refund_date = timezone.now()
            payment.save()
        except Payment.DoesNotExist:
            pass
        
        # Update tour availability
        tour_availability = booking.tour_availability
        tour_availability.spots_available += booking.participants
        tour_availability.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
