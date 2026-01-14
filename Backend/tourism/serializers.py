from rest_framework import serializers
# Remove GeoDjango serializer import for now
from .models import Region, TouristSite, SiteImage, BilingualContent


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', 'code', 'description', 'created_at', 'updated_at')


class SiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImage
        fields = ('id', 'image', 'caption', 'is_primary', 'created_at')


class BilingualContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilingualContent
        fields = ('id', 'language', 'title', 'description', 'created_at', 'updated_at')


class TouristSiteSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    images = SiteImageSerializer(many=True, read_only=True)
    bilingual_content = BilingualContentSerializer(many=True, read_only=True)
    
    class Meta:
        model = TouristSite
        fields = ('id', 'name', 'description', 'region', 'latitude', 'longitude', 'address',
                  'entrance_fee', 'opening_time', 'closing_time', 'is_active',
                  'created_at', 'updated_at', 'images', 'bilingual_content')


class TouristSiteListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    
    class Meta:
        model = TouristSite
        fields = ('id', 'name', 'description', 'region', 'latitude', 'longitude', 'address',
                  'entrance_fee', 'is_active', 'created_at')