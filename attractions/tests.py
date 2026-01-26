from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import AttractionCategory, Attraction

User = get_user_model()

class AttractionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.category = AttractionCategory.objects.create(
            name='Beach',
            description='Beach attractions'
        )
        self.attraction = Attraction.objects.create(
            name='Test Beach',
            description='A beautiful beach',
            category=self.category,
            address='123 Beach St',
            city='Beach City',
            state_province='Beach State',
            country='Beach Country',
            latitude='12.345678',
            longitude='98.765432',
            created_by=self.user
        )

    def test_attraction_list(self):
        """Test listing attractions"""
        response = self.client.get('/api/attractions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_attraction_detail(self):
        """Test getting attraction details"""
        response = self.client.get(f'/api/attractions/{self.attraction.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Beach')

    def test_attraction_creation(self):
        """Test creating a new attraction"""
        self.client.force_authenticate(user=self.user)
        new_attraction_data = {
            'name': 'New Attraction',
            'description': 'A new attraction',
            'category': self.category.id,
            'address': '456 New St',
            'city': 'New City',
            'state_province': 'New State',
            'country': 'New Country',
            'latitude': '11.111111',
            'longitude': '22.222222'
        }
        response = self.client.post('/api/attractions/create/', new_attraction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attraction.objects.count(), 2)
