from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tour, TourItinerary, TourAvailability
from .serializers import (
    TourSerializer, 
    TourCreateSerializer,
    TourItinerarySerializer,
    TourItineraryCreateSerializer,
    TourAvailabilitySerializer,
    TourAvailabilityCreateSerializer
)
from .filters import TourFilter

class TourListView(generics.ListAPIView):
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TourFilter
    search_fields = ['title', 'description', 'start_location', 'end_location']
    ordering_fields = ['title', 'price', 'start_date', 'created_at']
    ordering = ['-created_at']

class TourDetailView(generics.RetrieveAPIView):
    queryset = Tour.objects.filter(is_active=True)
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]

class TourCreateView(generics.CreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TourItineraryListView(generics.ListAPIView):
    serializer_class = TourItinerarySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tour_id = self.kwargs['tour_id']
        return TourItinerary.objects.filter(tour_id=tour_id)

class TourItineraryCreateView(generics.CreateAPIView):
    queryset = TourItinerary.objects.all()
    serializer_class = TourItineraryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class TourAvailabilityListView(generics.ListAPIView):
    serializer_class = TourAvailabilitySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tour_id = self.kwargs['tour_id']
        return TourAvailability.objects.filter(tour_id=tour_id, is_available=True)

class TourAvailabilityCreateView(generics.CreateAPIView):
    queryset = TourAvailability.objects.all()
    serializer_class = TourAvailabilityCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
