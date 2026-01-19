# Domain-Driven Design Implementation for NaTourCam

## Overview

This document describes the DDD (Domain-Driven Design) implementation that has been added to the NaTourCam project using a **Hybrid Approach**. The existing Django code continues to work, while new DDD layers have been added on top.

## What Has Been Implemented

### ✅ Shared Kernel (Foundation)

Located in [`Backend/shared/`](shared/)

1. **Base Domain Classes** ([`shared/domain/base.py`](shared/domain/base.py))
   - `DomainEvent` - Base for all domain events
   - `Entity` - Base for entities with identity
   - `AggregateRoot` - Base for aggregate roots with event handling
   - `ValueObject` - Base for immutable value objects
   - `IRepository` - Repository interface
   - `DomainService` - Base for domain services
   - `IEventBus` - Event bus interface
   - `DomainException` - Base for domain exceptions

2. **Common Value Objects** ([`shared/domain/value_objects.py`](shared/domain/value_objects.py))
   - `Email` - Email with validation
   - `PhoneNumber` - Phone number with validation
   - `Money` - Money with currency and operations (add, subtract, multiply)
   - `Location` - Geographic coordinates with validation
   - Type-safe IDs: `UserId`, `DestinationId`, `ReservationId`, `TransactionId`, `ReviewId`, `RegionId`

3. **Event Bus** ([`shared/infrastructure/event_bus.py`](shared/infrastructure/event_bus.py))
   - `InMemoryEventBus` - Event publishing and subscription
   - Global event bus instance

### ✅ Tourism Domain (Complete Implementation)

Located in [`Backend/tourism/`](tourism/)

#### Domain Layer ([`tourism/domain/`](tourism/domain/))

1. **Aggregates**
   - [`destination.py`](tourism/domain/destination.py) - `TouristDestination` aggregate with business logic
   - [`region.py`](tourism/domain/region.py) - `Region` aggregate

2. **Domain Events**
   - `DestinationCreated`, `DestinationActivated`, `DestinationDeactivated`, `DestinationUpdated`
   - `RegionCreated`, `RegionUpdated`

3. **Repository Interfaces** ([`repositories.py`](tourism/domain/repositories.py))
   - `IDestinationRepository` - Interface for destination data access
   - `IRegionRepository` - Interface for region data access

#### Infrastructure Layer ([`tourism/infrastructure/`](tourism/infrastructure/))

1. **Django Repository Implementations** ([`django_repositories.py`](tourism/infrastructure/django_repositories.py))
   - `DjangoDestinationRepository` - Adapts Django ORM to domain repository
   - `DjangoRegionRepository` - Adapts Django ORM to domain repository
   - Converts between Django models and domain aggregates
   - Publishes domain events after save

#### Application Layer ([`tourism/application/`](tourism/application/))

1. **Commands** ([`commands.py`](tourism/application/commands.py))
   - `CreateDestinationCommand` / `CreateDestinationHandler`
   - `UpdateDestinationCommand` / `UpdateDestinationHandler`
   - `ActivateDestinationCommand` / `ActivateDestinationHandler`
   - `DeactivateDestinationCommand` / `DeactivateDestinationHandler`
   - `CreateRegionCommand` / `CreateRegionHandler`
   - `UpdateRegionCommand` / `UpdateRegionHandler`

2. **Queries** ([`queries.py`](tourism/application/queries.py))
   - `GetDestinationQuery` / `GetDestinationHandler`
   - `GetAllDestinationsQuery` / `GetAllDestinationsHandler`
   - `GetDestinationsByRegionQuery` / `GetDestinationsByRegionHandler`
   - `SearchDestinationsQuery` / `SearchDestinationsHandler`
   - `GetRegionQuery` / `GetRegionHandler`
   - `GetAllRegionsQuery` / `GetAllRegionsHandler`

3. **Application Service** ([`services.py`](tourism/application/services.py))
   - `TourismApplicationService` - Facade for all tourism operations
   - Coordinates commands and queries
   - Single entry point for use cases

#### Presentation Layer

1. **DDD Views** ([`views_ddd.py`](tourism/views_ddd.py))
   - New API endpoints using DDD architecture
   - Uses application service instead of direct ORM
   - Demonstrates clean separation of concerns

2. **URL Routing** ([`urls_ddd.py`](tourism/urls_ddd.py))
   - Routes for DDD-based endpoints
   - Separate from existing URLs

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ views.py     │              │ views_ddd.py │            │
│  │ (existing)   │              │ (new DDD)    │            │
│  └──────┬───────┘              └──────┬───────┘            │
│         │                              │                     │
│         │ Direct ORM                   │ Uses Service        │
│         ↓                              ↓                     │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│                  ┌──────────────────────┐                   │
│                  │ TourismApplication   │                   │
│                  │      Service         │                   │
│                  └──────────┬───────────┘                   │
│                             │                                │
│         ┌───────────────────┼───────────────────┐          │
│         ↓                   ↓                   ↓            │
│  ┌──────────┐        ┌──────────┐       ┌──────────┐      │
│  │ Commands │        │ Queries  │       │   DTOs   │      │
│  └──────────┘        └──────────┘       └──────────┘      │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                            │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ TouristDestination│         │     Region       │         │
│  │   (Aggregate)    │         │   (Aggregate)    │         │
│  └──────────────────┘         └──────────────────┘         │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  Value Objects   │         │  Domain Events   │         │
│  └──────────────────┘         └──────────────────┘         │
│  ┌──────────────────┐                                       │
│  │   Repositories   │ (Interfaces)                          │
│  └──────────────────┘                                       │
├─────────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                        │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ Django           │         │   Event Bus      │         │
│  │ Repositories     │         │                  │         │
│  └────────┬─────────┘         └──────────────────┘         │
│           ↓                                                  │
│  ┌──────────────────┐                                       │
│  │ Django ORM       │                                       │
│  │ (models.py)      │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## How to Use

### Option 1: Use Existing Endpoints (No Changes)

Your existing endpoints continue to work:
- `GET /api/tourism/sites/` - List sites (existing)
- `GET /api/tourism/sites/{id}/` - Get site (existing)
- etc.

### Option 2: Use New DDD Endpoints

New DDD-based endpoints are available:
- `GET /api/tourism/ddd/destinations/` - List destinations (DDD)
- `GET /api/tourism/ddd/destinations/{id}/` - Get destination (DDD)
- `POST /api/tourism/ddd/destinations/create/` - Create destination (DDD)
- `PATCH /api/tourism/ddd/destinations/{id}/update/` - Update destination (DDD)
- `POST /api/tourism/ddd/destinations/{id}/activate/` - Activate (DDD)
- `POST /api/tourism/ddd/destinations/{id}/deactivate/` - Deactivate (DDD)
- `GET /api/tourism/ddd/destinations/search/?q=query` - Search (DDD)
- `GET /api/tourism/ddd/regions/` - List regions (DDD)

### Option 3: Use Application Service Directly

In your own code, you can use the application service:

```python
from tourism.application.services import get_tourism_service
from tourism.application.commands import CreateDestinationCommand
from decimal import Decimal

# Get the service
service = get_tourism_service()

# Create a destination
command = CreateDestinationCommand(
    name="Mount Cameroon",
    description="Active volcano and highest peak in West Africa",
    region_id=1,
    latitude=Decimal("4.2034"),
    longitude=Decimal("9.1706"),
    entrance_fee=Decimal("5000")
)
destination_id = service.create_destination(command)

# Query destinations
destinations = service.get_all_destinations()
for dest in destinations:
    print(f"{dest.name}: {dest.entrance_fee} {dest.currency}")
```

## Key Benefits

### 1. **Business Logic in Domain**
- Business rules are in domain aggregates, not scattered in views
- Example: `destination.activate()`, `destination.is_open_at(time)`

### 2. **Type Safety**
- Value objects prevent invalid data
- Example: `Money` ensures positive amounts, `Email` validates format

### 3. **Testability**
- Domain logic can be tested without database
- Application services can be tested with mock repositories

### 4. **Maintainability**
- Clear separation of concerns
- Easy to find where business logic lives

### 5. **Flexibility**
- Can change infrastructure (database, framework) without touching domain
- Domain events allow loose coupling between contexts

## Testing Examples

### Unit Test (Domain Logic)

```python
from tourism.domain.destination import TouristDestination
from shared.domain.value_objects import DestinationId, RegionId, Money
from decimal import Decimal

def test_destination_activation():
    # Arrange
    destination = TouristDestination(
        id=DestinationId(1),
        name="Test Site",
        description="Test description",
        region_id=RegionId(1),
        is_active=False
    )
    
    # Act
    destination.activate()
    
    # Assert
    assert destination.is_active == True
    assert len(destination.domain_events) == 1
    assert isinstance(destination.domain_events[0], DestinationActivated)
```

### Integration Test (Application Service)

```python
from tourism.application.services import get_tourism_service
from tourism.application.commands import CreateDestinationCommand

def test_create_destination():
    # Arrange
    service = get_tourism_service()
    command = CreateDestinationCommand(
        name="Test Destination",
        description="Test description",
        region_id=1
    )
    
    # Act
    destination_id = service.create_destination(command)
    
    # Assert
    destination = service.get_destination(destination_id)
    assert destination is not None
    assert destination.name == "Test Destination"
```

## Next Steps

### To Enable DDD URLs

Add to [`Backend/natourcam/urls.py`](natourcam/urls.py):

```python
from django.urls import path, include

urlpatterns = [
    # ... existing patterns ...
    path('api/tourism/', include('tourism.urls_ddd')),  # Add this line
]
```

### To Gradually Migrate

1. **Test DDD endpoints** - Verify they work correctly
2. **Update frontend** - Point to new DDD endpoints
3. **Migrate views** - Convert existing views to use application service
4. **Remove old code** - Once confident, remove direct ORM access

### To Extend to Other Contexts

Use the Tourism implementation as a template:

1. **Bookings Context**
   - Create `bookings/domain/` with `Reservation` aggregate
   - Create `bookings/application/` with commands and queries
   - Create `bookings/infrastructure/` with Django repositories

2. **Identity & Access Context**
   - Create `accounts/domain/` with `User` aggregate
   - Create `accounts/application/` with commands and queries
   - Create `accounts/infrastructure/` with Django repositories

## Domain Model Reference

### TouristDestination Aggregate

**Properties:**
- `id: DestinationId`
- `name: str`
- `description: str`
- `region_id: RegionId`
- `location: Optional[Location]`
- `entrance_fee: Money`
- `opening_time: Optional[time]`
- `closing_time: Optional[time]`
- `is_active: bool`
- `images: List[str]`

**Business Methods:**
- `create()` - Factory method
- `update_details()` - Update destination information
- `activate()` - Activate destination
- `deactivate()` - Deactivate destination
- `add_image()` - Add image
- `remove_image()` - Remove image
- `is_free_admission()` - Check if free
- `is_open_24_hours()` - Check if open 24/7
- `is_open_at(time)` - Check if open at specific time
- `can_be_booked()` - Check if bookable

**Domain Events:**
- `DestinationCreated`
- `DestinationActivated`
- `DestinationDeactivated`
- `DestinationUpdated`

### Region Aggregate

**Properties:**
- `id: RegionId`
- `name: str`
- `code: str`
- `description: str`

**Business Methods:**
- `create()` - Factory method
- `update_details()` - Update region information

**Domain Events:**
- `RegionCreated`
- `RegionUpdated`

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. `Backend/shared/` is in your Python path
2. All `__init__.py` files are present
3. Django can find the modules

### Database Issues

The DDD layer uses the existing Django models, so:
- No new migrations needed
- Existing data works as-is
- Both old and new endpoints access same data

### Event Bus Not Working

If domain events aren't firing:
1. Check that repositories call `get_event_bus().publish(event)`
2. Verify event handlers are registered in `apps.py`
3. Check logs for event publishing

## Resources

- **DDD Book**: "Domain-Driven Design" by Eric Evans
- **Implementation Book**: "Implementing Domain-Driven Design" by Vaughn Vernon
- **Planning Docs**: See [`plans/ddd-refactoring-plan.md`](../plans/ddd-refactoring-plan.md)

## Summary

This implementation provides:
- ✅ Complete DDD architecture for Tourism context
- ✅ Existing functionality preserved
- ✅ New DDD endpoints available
- ✅ Template for extending to other contexts
- ✅ Gradual migration path
- ✅ Full documentation

You can now:
1. Use new DDD endpoints immediately
2. Gradually migrate existing code
3. Extend pattern to other bounded contexts
4. Benefit from DDD principles while maintaining backward compatibility
