from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import TourOperator, UserProfile
from attractions.models import AttractionCategory, Attraction
from tours.models import Tour, TourAvailability
import random
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        # Get or create admin user
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin_user',
                'is_administrator': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            UserProfile.objects.get_or_create(
                user=admin,
                defaults={
                    'first_name': 'Admin',
                    'last_name': 'User'
                }
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))

        # Get or create tour operator
        operator_user, created = User.objects.get_or_create(
            email='operator@example.com',
            defaults={
                'username': 'tour_operator',
                'is_tour_operator': True
            }
        )
        if created:
            operator_user.set_password('operator123')
            operator_user.save()
            UserProfile.objects.get_or_create(
                user=operator_user,
                defaults={
                    'first_name': 'Tour',
                    'last_name': 'Operator'
                }
            )
            tour_operator, created = TourOperator.objects.get_or_create(
                user=operator_user,
                defaults={
                    'company_name': 'Adventure Tours Ltd',
                    'company_description': 'We provide amazing adventure tours across the country',
                    'business_license': 'TOUR123456',
                    'contact_person': 'John Manager',
                    'contact_email': 'john@adventuretours.com',
                    'contact_phone': '+1234567890',
                    'address': '123 Adventure Street, Tour City'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Created tour operator'))
            else:
                self.stdout.write(self.style.SUCCESS('Tour operator already exists'))
        else:
            self.stdout.write(self.style.SUCCESS('Tour operator already exists'))
            tour_operator, created = TourOperator.objects.get_or_create(
                user=operator_user,
                defaults={
                    'company_name': 'Adventure Tours Ltd',
                    'company_description': 'We provide amazing adventure tours across the country',
                    'business_license': 'TOUR123456',
                    'contact_person': 'John Manager',
                    'contact_email': 'john@adventuretours.com',
                    'contact_phone': '+1234567890',
                    'address': '123 Adventure Street, Tour City'
                }
            )

        # Get or create regular user
        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'username': 'regular_user'
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserProfile.objects.get_or_create(
                user=regular_user,
                defaults={
                    'first_name': 'Regular',
                    'last_name': 'User'
                }
            )
            self.stdout.write(self.style.SUCCESS('Created regular user'))
        else:
            self.stdout.write(self.style.SUCCESS('Regular user already exists'))

        # Create attraction categories
        categories_data = [
            ('Beach', 'Beautiful beaches and coastal areas'),
            ('Mountain', 'Mountain ranges and hiking trails'),
            ('Historical', 'Historical sites and monuments'),
            ('Cultural', 'Cultural experiences and traditions'),
            ('Wildlife', 'Wildlife reserves and national parks'),
            ('Adventure', 'Adventure sports and activities')
        ]
        
        for name, description in categories_data:
            category, created = AttractionCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Category already exists: {name}'))

        # Create attractions
        categories = AttractionCategory.objects.all()
        attractions_data = [
            ('Sunset Beach', 'A beautiful beach with golden sand and clear water', '123 Beach Road', 'Coastal City', 'Coastal State', 'Country A', 12.345678, 98.765432),
            ('Mountain Peak', 'Highest peak in the region with breathtaking views', '456 Mountain Trail', 'Mountain Town', 'Mountain State', 'Country A', 23.456789, 87.654321),
            ('Historic Castle', 'Ancient castle with rich history and architecture', '789 Castle Lane', 'History City', 'History State', 'Country A', 34.567890, 76.543210),
            ('Cultural Village', 'Traditional village showcasing local culture', '101 Culture Street', 'Culture Town', 'Culture State', 'Country A', 45.678901, 65.432109),
            ('Wildlife Reserve', 'Protected area with diverse wildlife', '202 Wildlife Road', 'Wildlife City', 'Wildlife State', 'Country A', 56.789012, 54.321098)
        ]
        
        tour_operator = TourOperator.objects.first()
        if tour_operator:
            for i, (name, description, address, city, state, country, lat, lng) in enumerate(attractions_data):
                attraction, created = Attraction.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': description,
                        'category': categories[i % len(categories)],
                        'address': address,
                        'city': city,
                        'state_province': state,
                        'country': country,
                        'latitude': lat,
                        'longitude': lng,
                        'created_by': tour_operator.user
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created attraction: {name}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Attraction already exists: {name}'))

        # Create tours
        attractions = Attraction.objects.all()
        tour_operator = TourOperator.objects.first()
        if tour_operator and attractions.exists():
            tours_data = [
                ('Beach Getaway', 'Relaxing beach vacation with water sports', 5, 20, 'moderate', 500.00, date.today(), date.today() + timedelta(days=30), 'Beach City', 'Beach City'),
                ('Mountain Trek', 'Challenging mountain hiking adventure', 7, 15, 'challenging', 800.00, date.today() + timedelta(days=10), date.today() + timedelta(days=40), 'Mountain Town', 'Mountain Town'),
                ('Historical Tour', 'Explore ancient historical sites', 3, 25, 'easy', 300.00, date.today() + timedelta(days=5), date.today() + timedelta(days=25), 'History City', 'History City')
            ]
            
            for title, description, duration, max_participants, difficulty, price, start_date, end_date, start_location, end_location in tours_data:
                tour, created = Tour.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'tour_operator': tour_operator,
                        'duration_days': duration,
                        'max_participants': max_participants,
                        'difficulty_level': difficulty,
                        'price': price,
                        'currency': 'USD',
                        'start_date': start_date,
                        'end_date': end_date,
                        'start_location': start_location,
                        'end_location': end_location,
                        'includes': 'Transportation, Accommodation, Meals, Guide',
                        'created_by': tour_operator.user
                    }
                )
                if created:
                    # Add random attractions to the tour
                    tour.attractions.set(random.sample(list(attractions), min(2, len(attractions))))
                    self.stdout.write(self.style.SUCCESS(f'Created tour: {title}'))
                    
                    # Create tour availability
                    for i in range(5):
                        availability_date = start_date + timedelta(days=i*7)
                        TourAvailability.objects.get_or_create(
                            tour=tour,
                            date=availability_date,
                            defaults={
                                'spots_available': max_participants,
                                'is_available': True
                            }
                        )
                else:
                    self.stdout.write(self.style.SUCCESS(f'Tour already exists: {title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))