from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from accounts.models import TourOperator
from tours.models import Tour, TourAvailability
from .models import Booking

User = get_user_model()

class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
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
        self.tour = Tour.objects.create(
            title='Test Tour',
            description='A test tour',
            tour_operator=self.tour_operator,
            duration_days=5,
            max_participants=10,
            difficulty_level='moderate',
            price=100.00,
            currency='USD',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            start_location='Test Start',
            end_location='Test End',
            includes='Test inclusions',
            created_by=self.tour_operator_user
        )
        self.tour_availability = TourAvailability.objects.create(
            tour=self.tour,
            date=date.today() + timedelta(days=7),
            spots_available=5
        )
        self.booking = Booking.objects.create(
            user=self.user,
            tour=self.tour,
            tour_availability=self.tour_availability,
            participants=2,
            total_price=200.00,
            currency='USD',
            emergency_contact_name='Emergency Contact',
            emergency_contact_phone='+1234567890'
        )

    def test_booking_list(self):
        """Test listing user bookings"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_booking_detail(self):
        """Test getting booking details"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.booking.id)

    def test_booking_creation(self):
        """Test creating a new booking"""
        self.client.force_authenticate(user=self.user)
        new_booking_data = {
            'tour': self.tour.id,
            'tour_availability': self.tour_availability.id,
            'participants': 1,
            'special_requests': 'None',
            'emergency_contact_name': 'New Contact',
            'emergency_contact_phone': '+1987654321',
            'participants_details': [
                {
                    'first_name': 'First',
                    'last_name': 'Last',
                    'date_of_birth': '1990-01-01',
                    'passport_number': 'P12345678',
                    'nationality': 'Test Country'
                }
            ]
        }
        response = self.client.post('/api/bookings/create/', new_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
