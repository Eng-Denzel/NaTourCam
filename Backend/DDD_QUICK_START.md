# DDD Quick Start Guide

## What Was Done

Your NaTourCam project now has **Domain-Driven Design (DDD) architecture** implemented using a **Hybrid Approach**. This means:

✅ **Existing code still works** - No breaking changes
✅ **New DDD layers added** - Clean architecture on top
✅ **Tourism context complete** - Fully functional example
✅ **Template for other contexts** - Easy to replicate

## Quick Test

### 1. Start the Server

```bash
cd Backend
python manage.py runserver
```

### 2. Test DDD Endpoints

**List all destinations (DDD):**
```bash
curl http://localhost:8000/api/tourism/ddd/destinations/
```

**Get a specific destination:**
```bash
curl http://localhost:8000/api/tourism/ddd/destinations/1/
```

**Search destinations:**
```bash
curl http://localhost:8000/api/tourism/ddd/destinations/search/?q=mount
```

**List regions:**
```bash
curl http://localhost:8000/api/tourism/ddd/regions/
```

### 3. Compare with Old Endpoints

**Old endpoint (still works):**
```bash
curl http://localhost:8000/api/tourism/sites/
```

**New DDD endpoint:**
```bash
curl http://localhost:8000/api/tourism/ddd/destinations/
```

Both return the same data, but the DDD endpoint uses clean architecture!

## File Structure

```
Backend/
├── shared/                          # ✅ NEW: Shared Kernel
│   ├── domain/
│   │   ├── base.py                 # Base DDD classes
│   │   └── value_objects.py        # Common value objects
│   └── infrastructure/
│       └── event_bus.py            # Event bus
│
├── tourism/                         # ✅ ENHANCED: Tourism with DDD
│   ├── models.py                   # Existing Django models (kept)
│   ├── views.py                    # Existing views (kept)
│   ├── urls.py                     # Existing URLs (kept)
│   ├── domain/                     # ✅ NEW: Domain layer
│   │   ├── destination.py          # TouristDestination aggregate
│   │   ├── region.py               # Region aggregate
│   │   └── repositories.py         # Repository interfaces
│   ├── application/                # ✅ NEW: Application layer
│   │   ├── commands.py             # Command handlers
│   │   ├── queries.py              # Query handlers
│   │   └── services.py             # Application service
│   ├── infrastructure/             # ✅ NEW: Infrastructure layer
│   │   └── django_repositories.py  # Django ORM adapters
│   ├── views_ddd.py                # ✅ NEW: DDD-based views
│   └── urls_ddd.py                 # ✅ NEW: DDD URLs
│
├── accounts/                        # Existing (can be enhanced later)
├── bookings/                        # Existing (can be enhanced later)
└── natourcam/
    └── urls.py                      # ✅ UPDATED: Includes DDD routes
```

## Key Concepts

### 1. Domain Layer (Business Logic)

**TouristDestination Aggregate:**
```python
from tourism.domain.destination import TouristDestination
from shared.domain.value_objects import DestinationId, RegionId, Money
from decimal import Decimal

# Create a destination with business logic
destination = TouristDestination.create(
    id=DestinationId(1),
    name="Mount Cameroon",
    description="Active volcano",
    region_id=RegionId(1),
    entrance_fee=Money(Decimal("5000"), "XAF")
)

# Business methods
destination.activate()
destination.is_open_at(time(14, 30))  # Check if open at 2:30 PM
destination.is_free_admission()       # Check if free
```

### 2. Application Layer (Use Cases)

**Using the Application Service:**
```python
from tourism.application.services import get_tourism_service
from tourism.application.commands import CreateDestinationCommand

service = get_tourism_service()

# Create a destination
command = CreateDestinationCommand(
    name="Kribi Beach",
    description="Beautiful beach",
    region_id=2
)
destination_id = service.create_destination(command)

# Query destinations
destinations = service.get_all_destinations()
```

### 3. Infrastructure Layer (Technical Details)

**Repository adapts Django ORM to domain:**
```python
from tourism.infrastructure.django_repositories import get_destination_repository

repo = get_destination_repository()
destination = repo.get_by_id(DestinationId(1))
destination.activate()
repo.save(destination)  # Saves to Django ORM and publishes events
```

## Benefits You Get

### 1. **Type Safety**
```python
# Before (error-prone)
entrance_fee = -100  # Oops, negative!

# After (safe)
entrance_fee = Money(Decimal("-100"), "XAF")  # Raises InvalidMoneyError
```

### 2. **Business Logic in Domain**
```python
# Before (scattered in views)
if site.opening_time and site.closing_time:
    if site.opening_time <= check_time <= site.closing_time:
        return True

# After (in domain)
destination.is_open_at(check_time)  # Clear and reusable
```

### 3. **Testable Without Database**
```python
# Test domain logic without Django
def test_destination_activation():
    destination = TouristDestination(...)
    destination.activate()
    assert destination.is_active == True
```

### 4. **Domain Events**
```python
# Automatically published when destination is created
destination = TouristDestination.create(...)
# DestinationCreated event is added to domain_events
# Event bus publishes it when repository saves
```

## Next Steps

### Option 1: Use DDD Endpoints Now

Update your frontend to use new endpoints:
- Change `/api/tourism/sites/` → `/api/tourism/ddd/destinations/`
- Enjoy cleaner architecture!

### Option 2: Gradually Migrate

1. Keep using old endpoints
2. Slowly update views to use application service
3. Eventually remove old code

### Option 3: Extend to Other Contexts

Use Tourism as a template:

**For Bookings:**
1. Create `bookings/domain/reservation.py`
2. Create `bookings/application/commands.py`
3. Create `bookings/infrastructure/django_repositories.py`
4. Create `bookings/views_ddd.py`

**For Accounts:**
1. Create `accounts/domain/user.py`
2. Create `accounts/application/commands.py`
3. Create `accounts/infrastructure/django_repositories.py`
4. Create `accounts/views_ddd.py`

## Common Tasks

### Create a New Destination (Admin)

```bash
curl -X POST http://localhost:8000/api/tourism/ddd/destinations/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Waza National Park",
    "description": "Wildlife reserve",
    "region_id": 3,
    "latitude": "11.4",
    "longitude": "14.5",
    "entrance_fee": "10000"
  }'
```

### Update a Destination

```bash
curl -X PATCH http://localhost:8000/api/tourism/ddd/destinations/1/update/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "entrance_fee": "7500"
  }'
```

### Activate/Deactivate

```bash
# Activate
curl -X POST http://localhost:8000/api/tourism/ddd/destinations/1/activate/ \
  -H "Authorization: Token YOUR_TOKEN"

# Deactivate
curl -X POST http://localhost:8000/api/tourism/ddd/destinations/1/deactivate/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Troubleshooting

### "Module not found" Error

Make sure `Backend/shared/` is in your Python path. Django should handle this automatically.

### "No such table" Error

The DDD layer uses existing Django models, so run migrations if needed:
```bash
python manage.py migrate
```

### Domain Events Not Firing

Check that event handlers are registered in `tourism/apps.py`:
```python
def ready(self):
    from . import event_handlers  # Import to register
```

## Documentation

- **Full Implementation Guide**: [`DDD_IMPLEMENTATION_README.md`](DDD_IMPLEMENTATION_README.md)
- **Refactoring Plan**: [`../plans/ddd-refactoring-plan.md`](../plans/ddd-refactoring-plan.md)
- **Implementation Status**: [`../plans/ddd-implementation-status.md`](../plans/ddd-implementation-status.md)

## Summary

You now have:
- ✅ **Working DDD architecture** for Tourism
- ✅ **Backward compatibility** with existing code
- ✅ **Clean separation** of concerns
- ✅ **Type-safe** value objects
- ✅ **Testable** domain logic
- ✅ **Event-driven** architecture
- ✅ **Template** for other contexts

**Start using it today!** 🚀
