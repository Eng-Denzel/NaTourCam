from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AttractionCategory, Attraction, AttractionReview
from .serializers import (
    AttractionCategorySerializer, 
    AttractionSerializer, 
    AttractionCreateSerializer,
    AttractionReviewSerializer,
    AttractionReviewCreateSerializer
)
from .filters import AttractionFilter

class AttractionCategoryListView(generics.ListAPIView):
    queryset = AttractionCategory.objects.all()
    serializer_class = AttractionCategorySerializer
    permission_classes = [permissions.AllowAny]

class AttractionListView(generics.ListAPIView):
    queryset = Attraction.objects.filter(is_active=True)
    serializer_class = AttractionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AttractionFilter
    search_fields = ['name', 'description', 'city', 'state_province', 'country']
    ordering_fields = ['name', 'created_at', 'average_rating']
    ordering = ['-created_at']

class AttractionDetailView(generics.RetrieveAPIView):
    queryset = Attraction.objects.filter(is_active=True)
    serializer_class = AttractionSerializer
    permission_classes = [permissions.AllowAny]

class AttractionCreateView(generics.CreateAPIView):
    queryset = Attraction.objects.all()
    serializer_class = AttractionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class AttractionReviewListView(generics.ListAPIView):
    serializer_class = AttractionReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        attraction_id = self.kwargs['attraction_id']
        return AttractionReview.objects.filter(attraction_id=attraction_id)

class AttractionReviewCreateView(generics.CreateAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
