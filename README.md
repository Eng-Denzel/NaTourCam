# NaTourCam - Nationwide Smart Tourism Platform

NaTourCam is a comprehensive Django-based backend system for a smart tourism platform that allows users to discover, book, and manage tourist attractions and tours across the nation.

## Features

- User authentication and account management
- Search and discovery of tourist attractions
- Tour package creation and management
- Booking system with payment integration
- Real-time notifications
- Analytics dashboard for administrators
- RESTful API architecture

## Technology Stack

- **Backend**: Django 4.2 with Django REST Framework
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL
- **Real-time**: Django Channels with Redis
- **Authentication**: Token-based authentication
- **Image Processing**: Pillow

## Project Structure

```
NaTourCam/
├── accounts/          # User management and authentication
├── attractions/       # Attraction discovery and management
├── tours/             # Tour package creation and management
├── bookings/          # Booking system and payment processing
├── notifications/     # Real-time notifications
├── analytics/         # Analytics and reporting
├── NaTourCam/         # Main project settings
└── manage.py          # Django management script
```

## Domain Models

### Accounts
- User (Custom user model with email as username)
- UserProfile (Extended user information)
- TourOperator (Business entity for tour operators)

### Attractions
- AttractionCategory (Types of attractions)
- Attraction (Tourist attractions)
- AttractionImage (Images for attractions)
- AttractionReview (User reviews for attractions)

### Tours
- Tour (Tour packages)
- TourImage (Images for tours)
- TourItinerary (Daily itinerary for tours)
- TourAvailability (Availability dates for tours)

### Bookings
- Booking (Tour bookings)
- BookingParticipant (Details of participants)
- Payment (Payment transactions)

### Notifications
- Notification (User notifications)
- NotificationPreference (User notification preferences)

### Analytics
- UserAnalytics (User behavior analytics)
- AttractionAnalytics (Attraction performance analytics)
- TourAnalytics (Tour performance analytics)
- BookingAnalytics (Booking trends analytics)
- SystemAnalytics (Overall system analytics)

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET /api/accounts/profile/` - Get user profile
- `PUT /api/accounts/profile/` - Update user profile
- `GET /api/accounts/tour-operator/` - Get tour operator profile
- `POST /api/accounts/tour-operator/create/` - Create tour operator profile

### Attractions
- `GET /api/attractions/categories/` - List attraction categories
- `GET /api/attractions/` - List attractions with filtering
- `GET /api/attractions/{id}/` - Get attraction details
- `POST /api/attractions/create/` - Create new attraction (authenticated)
- `GET /api/attractions/{id}/reviews/` - List reviews for attraction
- `POST /api/attractions/reviews/create/` - Create attraction review

### Tours
- `GET /api/tours/` - List tours with filtering
- `GET /api/tours/{id}/` - Get tour details
- `POST /api/tours/create/` - Create new tour (tour operators only)
- `GET /api/tours/{id}/itinerary/` - Get tour itinerary
- `POST /api/tours/itinerary/create/` - Add to tour itinerary
- `GET /api/tours/{id}/availability/` - Get tour availability
- `POST /api/tours/availability/create/` - Set tour availability

### Bookings
- `GET /api/bookings/` - List user bookings
- `GET /api/bookings/{id}/` - Get booking details
- `POST /api/bookings/create/` - Create new booking
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `POST /api/bookings/payment/create/` - Process payment for booking

### Notifications
- `GET /api/notifications/` - List user notifications
- `GET /api/notifications/{id}/` - Get notification details
- `PUT /api/notifications/{id}/` - Mark notification as read
- `GET /api/notifications/unread-count/` - Get unread notification count
- `POST /api/notifications/mark-all-read/` - Mark all notifications as read
- `GET /api/notifications/preferences/` - Get notification preferences
- `PUT /api/notifications/preferences/` - Update notification preferences

### Analytics
- `GET /api/analytics/user/` - Get user analytics
- `GET /api/analytics/attraction/{id}/` - Get attraction analytics
- `GET /api/analytics/tour/{id}/` - Get tour analytics
- `GET /api/analytics/admin/dashboard/` - Get admin dashboard data

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NaTourCam
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://127.0.0.1:6379/0
```

### Settings

The main settings are configured in `NaTourCam/settings.py`:
- Database configuration
- Authentication settings
- CORS settings for frontend integration
- Channels configuration for real-time features
- Media and static files configuration

## Deployment

### Production Settings

For production deployment, update the following settings:
- Set `DEBUG=False`
- Use a production database (PostgreSQL recommended)
- Configure proper static and media file storage
- Set up a proper web server (Nginx) and WSGI server (Gunicorn)
- Configure SSL/HTTPS
- Set up Redis for Channels
- Use environment variables for sensitive settings

### Docker Deployment

A Docker configuration can be added for containerized deployment:

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

2. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - .:/app
       environment:
         - DEBUG=True
       depends_on:
         - redis
         - db
   
     redis:
       image: redis:7
   
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=naturcam
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.