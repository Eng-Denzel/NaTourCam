from rest_framework import serializers
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
    images = SiteImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = TouristSite
        fields = ('id', 'name', 'description', 'region', 'latitude', 'longitude', 'address',
                  'entrance_fee', 'is_active', 'created_at', 'images')


class AdminTouristSiteUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin to update tourist site status and details"""
    
    class Meta:
        model = TouristSite
        fields = ('id', 'name', 'description', 'region', 'latitude', 'longitude', 'address',
                  'entrance_fee', 'opening_time', 'closing_time', 'is_active')
        read_only_fields = ('id',)
    
    def update(self, instance, validated_data):
        # Update all fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminTouristSiteCreateSerializer(serializers.ModelSerializer):
    """Serializer for admin to create new tourist sites"""
    
    class Meta:
        model = TouristSite
        fields = ('id', 'name', 'description', 'region', 'latitude', 'longitude', 'address',
                  'entrance_fee', 'opening_time', 'closing_time', 'is_active')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        # Create new tourist site
        site = TouristSite.objects.create(**validated_data)
        return site