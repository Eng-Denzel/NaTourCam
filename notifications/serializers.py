from rest_framework import serializers
from .models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 
                  'created_at', 'read_at']
        read_only_fields = ['id', 'created_at', 'read_at']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['email_notifications', 'sms_notifications', 'push_notifications',
                  'booking_notifications', 'payment_notifications', 'tour_updates',
                  'promotions']