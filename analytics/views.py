from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import UserAnalytics, AttractionAnalytics, TourAnalytics, BookingAnalytics, SystemAnalytics
from .serializers import (
    UserAnalyticsSerializer, 
    AttractionAnalyticsSerializer, 
    TourAnalyticsSerializer, 
    BookingAnalyticsSerializer, 
    SystemAnalyticsSerializer
)
from accounts.models import User
from attractions.models import Attraction
from tours.models import Tour
from bookings.models import Booking

class UserAnalyticsView(generics.RetrieveAPIView):
    serializer_class = UserAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        analytics, created = UserAnalytics.objects.get_or_create(user=self.request.user)
        return analytics

class AttractionAnalyticsView(generics.RetrieveAPIView):
    serializer_class = AttractionAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only tour operators can view analytics for their attractions
        return AttractionAnalytics.objects.filter(
            attraction__created_by=self.request.user
        )
    
    def get_object(self):
        queryset = self.get_queryset()
        attraction_id = self.kwargs['attraction_id']
        analytics = generics.get_object_or_404(queryset, attraction_id=attraction_id)
        return analytics

class TourAnalyticsView(generics.RetrieveAPIView):
    serializer_class = TourAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only tour operators can view analytics for their tours
        return TourAnalytics.objects.filter(
            tour__created_by=self.request.user
        )
    
    def get_object(self):
        queryset = self.get_queryset()
        tour_id = self.kwargs['tour_id']
        analytics = generics.get_object_or_404(queryset, tour_id=tour_id)
        return analytics

class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        # Get date range (last 30 days by default)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # System analytics
        total_users = User.objects.count()
        total_attractions = Attraction.objects.count()
        total_tours = Tour.objects.count()
        total_bookings = Booking.objects.count()
        total_revenue = Booking.objects.filter(status='confirmed').aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Recent booking analytics
        recent_bookings = BookingAnalytics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            total_bookings=Sum('total_bookings'),
            total_revenue=Sum('total_revenue')
        )
        
        data = {
            'system': {
                'total_users': total_users,
                'total_attractions': total_attractions,
                'total_tours': total_tours,
                'total_bookings': total_bookings,
                'total_revenue': total_revenue,
            },
            'recent': {
                'total_bookings': recent_bookings['total_bookings'] or 0,
                'total_revenue': recent_bookings['total_revenue'] or 0,
            }
        }
        
        return Response(data)
