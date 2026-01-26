from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Notification

User = get_user_model()

class NotificationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='system_alert'
        )

    def test_notification_list(self):
        """Test listing user notifications"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_notification_detail(self):
        """Test getting notification details"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Notification')

    def test_mark_notification_as_read(self):
        """Test marking a notification as read"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'is_read': True
        }
        response = self.client.put(f'/api/notifications/{self.notification.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
