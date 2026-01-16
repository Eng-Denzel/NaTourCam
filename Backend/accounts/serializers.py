from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                  'phone_number', 'language', 'date_of_birth', 'is_verified', 
                  'created_at', 'updated_at', 'password')
        read_only_fields = ('id', 'is_verified', 'created_at', 'updated_at')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False, 'allow_blank': True},
            'language': {'required': False},
            'date_of_birth': {'required': False, 'allow_null': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Remove password from validated_data if present
        password = validated_data.pop('password', None)
        
        # Check for unique email if being updated
        email = validated_data.get('email')
        if email and email != instance.email:
            if User.objects.filter(email=email).exclude(id=instance.id).exists():
                raise serializers.ValidationError({'email': 'This email is already in use.'})
        
        # Check for unique username if being updated
        username = validated_data.get('username')
        if username and username != instance.username:
            if User.objects.filter(username=username).exclude(id=instance.id).exists():
                raise serializers.ValidationError({'username': 'This username is already taken.'})
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Only update password if provided and not empty
        if password and password.strip():
            instance.set_password(password)
        
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 
                  'phone_number', 'language', 'date_of_birth', 
                  'password', 'password_confirm')
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user