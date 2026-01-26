from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import TourOperator
from attractions.models import AttractionCategory, Attraction
from tours.models import Tour
from .models import UserAnalytics, AttractionAnalytics, TourAnalytics

User = get_user_model()

class AnalyticsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword123',
            is_staff=True,
            is_administrator=True
        )
        self.tour_operator_user = User.objects.create_user(
            username='touroperator',
            email='operator@example.com',
            password='testpassword123',
            is_tour_operator=True
        )
        self.tour_operator = TourOperator.objects.create(
            user=self.tour_operator_user,
            company_name='Test Company',
            company_description='Test company description',
            business_license='123456',
            contact_person='Test Person',
            contact_email='contact@test.com',
            contact_phone='+1234567890',
            address='123 Test St'
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
            created_by=self.tour_operator_user
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
            created_by=self.tour_operator_user
        )
        self.user_analytics = UserAnalytics.objects.create(
            user=self.user,
            total_bookings=5,
            total_spent=500.00
        )
        self.attraction_analytics = AttractionAnalytics.objects.create(
            attraction=self.attraction,
            total_views=100,
            total_bookings=10,
            average_rating=4.5,
            total_reviews=8
        )
        self.tour_analytics = TourAnalytics.objects.create(
            tour=self.tour,
            total_bookings=15,
            total_revenue=1500.00,
            average_rating=4.2,
            total_reviews=12
        )

    def test_user_analytics(self):
        """Test user analytics endpoint"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/analytics/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_bookings'], 5)

    def test_attraction_analytics(self):
        """Test attraction analytics endpoint"""
        self.client.force_authenticate(user=self.tour_operator_user)
        response = self.client.get(f'/api/analytics/attraction/{self.attraction.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_views'], 100)

    def test_tour_analytics(self):
        """Test tour analytics endpoint"""
        self.client.force_authenticate(user=self.tour_operator_user)
        response = self.client.get(f'/api/analytics/tour/{self.tour.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_bookings'], 15)

    def test_admin_dashboard(self):
        """Test admin dashboard endpoint"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/analytics/admin/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('system', response.data)
        self.assertIn('recent', response.data)
