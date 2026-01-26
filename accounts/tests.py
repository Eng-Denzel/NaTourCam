from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile

User = get_user_model()

class AccountAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone_number': '+1234567890'
        }
        self.user = User.objects.create_user(**self.user_data)
        # Create a profile for the user
        UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User'
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        new_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'phone_number': '+1987654321'
        }
        response = self.client.post('/api/accounts/register/', new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        """Test user login endpoint"""
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/accounts/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_user_profile_retrieval(self):
        """Test user profile retrieval"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/accounts/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_profile_update(self):
        """Test user profile update"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '+1111111111',
            'profile': {
                'first_name': 'Updated',
                'last_name': 'User'
            }
        }
        response = self.client.put('/api/accounts/profile/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, '+1111111111')
