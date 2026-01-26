from rest_framework import serializers
from .models import Tour, TourImage, TourItinerary, TourAvailability

class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['id', 'image', 'caption', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class TourItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItinerary
        fields = ['id', 'day_number', 'title', 'description', 'location', 'accommodation', 'meals']
        read_only_fields = ['id']

class TourAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAvailability
        fields = ['id', 'date', 'spots_available', 'is_available']
        read_only_fields = ['id']

class TourSerializer(serializers.ModelSerializer):
    tour_operator_name = serializers.CharField(source='tour_operator.company_name', read_only=True)
    images = TourImageSerializer(many=True, read_only=True)
    itinerary = TourItinerarySerializer(many=True, read_only=True)
    availability = TourAvailabilitySerializer(many=True, read_only=True)
    attractions = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = ['id', 'title', 'description', 'tour_operator', 'tour_operator_name',
                  'attractions', 'duration_days', 'max_participants', 'difficulty_level',
                  'price', 'currency', 'start_date', 'end_date', 'start_location',
                  'end_location', 'includes', 'excludes', 'is_active', 'images',
                  'itinerary', 'availability', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_attractions(self, obj):
        from attractions.serializers import AttractionSerializer
        return AttractionSerializer(obj.attractions.all(), many=True).data

class TourCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'tour_operator', 'attractions',
                  'duration_days', 'max_participants', 'difficulty_level',
                  'price', 'currency', 'start_date', 'end_date', 'start_location',
                  'end_location', 'includes', 'excludes']
        
    def validate_tour_operator(self, value):
        # Ensure the user is the owner of the tour operator
        request = self.context.get('request')
        if request and request.user != value.user:
            raise serializers.ValidationError("You can only create tours for your own tour operator.")
        return value

class TourItineraryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourItinerary
        fields = ['tour', 'day_number', 'title', 'description', 'location', 'accommodation', 'meals']
        
    def validate_tour(self, value):
        # Ensure the user is the owner of the tour
        request = self.context.get('request')
        if request and request.user != value.created_by:
            raise serializers.ValidationError("You can only add itinerary items to your own tours.")
        return value

class TourAvailabilityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAvailability
        fields = ['tour', 'date', 'spots_available']
        
    def validate_tour(self, value):
        # Ensure the user is the owner of the tour
        request = self.context.get('request')
        if request and request.user != value.created_by:
            raise serializers.ValidationError("You can only set availability for your own tours.")
        return value