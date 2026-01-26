from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import TourOperator
from .models import Tour

User = get_user_model()

class TourAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            is_tour_operator=True
        )
        self.tour_operator = TourOperator.objects.create(
            user=self.user,
            company_name='Test Company',
            company_description='Test company description',
            business_license='123456',
            contact_person='Test Person',
            contact_email='contact@test.com',
            contact_phone='+1234567890',
            address='123 Test St'
        )
        self.tour = Tour.objects.create(
            title='Test Tour',
            description='A test tour',
            tour_operator=self.tour_operator,
            duration_days=5,
            max_participants=10,
            difficulty_level='moderate',
            price=100.00,
            currency='USD',
            start_date='2026-01-01',
            end_date='2026-12-31',
            start_location='Test Start',
            end_location='Test End',
            includes='Test inclusions',
            created_by=self.user
        )

    def test_tour_list(self):
        """Test listing tours"""
        response = self.client.get('/api/tours/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_tour_detail(self):
        """Test getting tour details"""
        response = self.client.get(f'/api/tours/{self.tour.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Tour')

    def test_tour_creation(self):
        """Test creating a new tour"""
        self.client.force_authenticate(user=self.user)
        new_tour_data = {
            'title': 'New Tour',
            'description': 'A new tour',
            'tour_operator': self.tour_operator.id,
            'duration_days': 3,
            'max_participants': 5,
            'difficulty_level': 'easy',
            'price': 50.00,
            'currency': 'USD',
            'start_date': '2026-06-01',
            'end_date': '2026-06-30',
            'start_location': 'New Start',
            'end_location': 'New End',
            'includes': 'New inclusions'
        }
        response = self.client.post('/api/tours/create/', new_tour_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tour.objects.count(), 2)
