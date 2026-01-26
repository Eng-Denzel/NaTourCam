from rest_framework import serializers
from .models import AttractionCategory, Attraction, AttractionImage, AttractionReview

class AttractionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionCategory
        fields = ['id', 'name', 'description', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']

class AttractionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionImage
        fields = ['id', 'image', 'caption', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class AttractionReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AttractionReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'is_verified', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class AttractionSerializer(serializers.ModelSerializer):
    category = AttractionCategorySerializer(read_only=True)
    images = AttractionImageSerializer(many=True, read_only=True)
    reviews = AttractionReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'description', 'category', 'address', 'city', 
                  'state_province', 'country', 'latitude', 'longitude', 
                  'contact_phone', 'contact_email', 'website', 'opening_time', 
                  'closing_time', 'entry_fee', 'is_active', 'images', 'reviews',
                  'average_rating', 'total_reviews', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()

class AttractionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['name', 'description', 'category', 'address', 'city', 
                  'state_province', 'country', 'latitude', 'longitude', 
                  'contact_phone', 'contact_email', 'website', 'opening_time', 
                  'closing_time', 'entry_fee']
        
class AttractionReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionReview
        fields = ['attraction', 'rating', 'comment']
        read_only_fields = ['user']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)