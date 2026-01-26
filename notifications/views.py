from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationPreferenceSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, is_archived=False)

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        if 'is_read' in request.data and request.data['is_read']:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        return Response(self.get_serializer(notification).data)

class UnreadNotificationCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False, 
            is_archived=False
        ).count()
        return Response({'unread_count': count})

class MarkAllNotificationsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        Notification.objects.filter(
            recipient=request.user, 
            is_read=False, 
            is_archived=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'message': 'All notifications marked as read'})

class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference
