from rest_framework import generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Remove GeoDjango imports for now
from django_filters.rest_framework import DjangoFilterBackend
from .models import TouristSite, BilingualContent
from .serializers import TouristSiteListSerializer, TouristSiteSerializer, BilingualContentSerializer


class TouristSiteListView(generics.ListAPIView):
    queryset = TouristSite.objects.filter(is_active=True)
    serializer_class = TouristSiteListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region']
    search_fields = ['name', 'description', 'address']


class TouristSiteDetailView(generics.RetrieveAPIView):
    queryset = TouristSite.objects.filter(is_active=True)
    serializer_class = TouristSiteSerializer
    permission_classes = [AllowAny]


# Remove geospatial functionality for now


class BilingualContentView(generics.ListAPIView):
    queryset = BilingualContent.objects.all()
    serializer_class = BilingualContentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site', 'language']
