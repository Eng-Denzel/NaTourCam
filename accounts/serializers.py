from rest_framework import serializers
from .models import User, UserProfile, TourOperator

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'country', 'city', 'preferred_language']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'date_of_birth', 
                  'is_tour_operator', 'is_administrator', 'profile', 'created_at']
        read_only_fields = ['id', 'created_at']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile if provided
        if profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance

class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourOperator
        fields = ['id', 'company_name', 'company_description', 'business_license',
                  'contact_person', 'contact_email', 'contact_phone', 'address',
                  'website', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'date_of_birth', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
            
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()