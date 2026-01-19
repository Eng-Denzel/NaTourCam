# DDD Extension Guide - Bookings & Accounts Contexts

## Overview

This guide shows how to extend the DDD implementation from Tourism to Bookings and Accounts contexts. The Tourism context serves as a complete, working template.

## What's Already Done

✅ **Shared Kernel** - Complete foundation
✅ **Tourism Context** - Fully implemented with all layers
✅ **Documentation** - Comprehensive guides and examples

## Extending to Bookings Context

### Step 1: Create Domain Layer

**File: `Backend/bookings/domain/reservation.py`**

```python
"""
Reservation aggregate root - Manages booking lifecycle
"""
from typing import Optional
from datetime import date
from decimal import Decimal
from shared.domain.base import AggregateRoot, DomainEvent, DomainException
from shared.domain.value_objects import ReservationId, UserId, DestinationId, Money


# Domain Events
class ReservationCreated(DomainEvent):
    def __init__(self, reservation_id: ReservationId, user_id: UserId, destination_id: DestinationId):
        super().__init__()
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.destination_id = destination_id


class ReservationConfirmed(DomainEvent):
    def __init__(self, reservation_id: ReservationId):
        super().__init__()
        self.reservation_id = reservation_id


class ReservationCancelled(DomainEvent):
    def __init__(self, reservation_id: ReservationId, reason: str):
        super().__init__()
        self.reservation_id = reservation_id
        self.reason = reason


class ReservationCompleted(DomainEvent):
    def __init__(self, reservation_id: ReservationId):
        super().__init__()
        self.reservation_id = reservation_id


# Value Objects
class BookingStatus:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    
    VALID_STATUSES = [PENDING, CONFIRMED, CANCELLED, COMPLETED]
    
    def __init__(self, value: str):
        if value not in self.VALID_STATUSES:
            raise DomainException(f"Invalid booking status: {value}")
        self.value = value
    
    def is_pending(self) -> bool:
        return self.value == self.PENDING
    
    def is_confirmed(self) -> bool:
        return self.value == self.CONFIRMED
    
    def is_cancelled(self) -> bool:
        return self.value == self.CANCELLED
    
    def is_completed(self) -> bool:
        return self.value == self.COMPLETED


# Aggregate Root
class Reservation(AggregateRoot):
    """
    Reservation aggregate root.
    Manages the lifecycle of a booking from creation to completion.
    """
    
    def __init__(
        self,
        id: ReservationId,
        user_id: UserId,
        destination_id: DestinationId,
        booking_date: date,
        number_of_visitors: int,
        total_price: Money,
        status: BookingStatus,
        special_requests: str = ""
    ):
        super().__init__(id)
        self._user_id = user_id
        self._destination_id = destination_id
        self._booking_date = booking_date
        self._number_of_visitors = number_of_visitors
        self._total_price = total_price
        self._status = status
        self._special_requests = special_requests
        
        self._validate()
    
    @classmethod
    def create(
        cls,
        id: ReservationId,
        user_id: UserId,
        destination_id: DestinationId,
        booking_date: date,
        number_of_visitors: int,
        total_price: Money,
        special_requests: str = ""
    ) -> 'Reservation':
        """Factory method to create a new reservation"""
        reservation = cls(
            id=id,
            user_id=user_id,
            destination_id=destination_id,
            booking_date=booking_date,
            number_of_visitors=number_of_visitors,
            total_price=total_price,
            status=BookingStatus(BookingStatus.PENDING),
            special_requests=special_requests
        )
        
        reservation.add_domain_event(
            ReservationCreated(id, user_id, destination_id)
        )
        
        return reservation
    
    def _validate(self):
        """Validate reservation invariants"""
        if self._number_of_visitors <= 0:
            raise DomainException("Number of visitors must be positive")
        
        if self._booking_date < date.today():
            raise DomainException("Cannot book for past dates")
        
        if self._total_price.is_zero():
            raise DomainException("Total price must be greater than zero")
    
    # Properties
    @property
    def user_id(self) -> UserId:
        return self._user_id
    
    @property
    def destination_id(self) -> DestinationId:
        return self._destination_id
    
    @property
    def booking_date(self) -> date:
        return self._booking_date
    
    @property
    def number_of_visitors(self) -> int:
        return self._number_of_visitors
    
    @property
    def total_price(self) -> Money:
        return self._total_price
    
    @property
    def status(self) -> BookingStatus:
        return self._status
    
    @property
    def special_requests(self) -> str:
        return self._special_requests
    
    # Business methods
    def confirm(self):
        """Confirm the reservation"""
        if not self._status.is_pending():
            raise DomainException("Only pending reservations can be confirmed")
        
        self._status = BookingStatus(BookingStatus.CONFIRMED)
        self.add_domain_event(ReservationConfirmed(self.id))
    
    def cancel(self, reason: str = ""):
        """Cancel the reservation"""
        if self._status.is_completed():
            raise DomainException("Cannot cancel completed reservations")
        
        if self._status.is_cancelled():
            return  # Already cancelled
        
        self._status = BookingStatus(BookingStatus.CANCELLED)
        self.add_domain_event(ReservationCancelled(self.id, reason))
    
    def complete(self):
        """Mark reservation as completed"""
        if not self._status.is_confirmed():
            raise DomainException("Only confirmed reservations can be completed")
        
        if self._booking_date > date.today():
            raise DomainException("Cannot complete future reservations")
        
        self._status = BookingStatus(BookingStatus.COMPLETED)
        self.add_domain_event(ReservationCompleted(self.id))
    
    def can_be_modified(self) -> bool:
        """Check if reservation can be modified"""
        return self._status.is_pending()
    
    def can_be_cancelled(self) -> bool:
        """Check if reservation can be cancelled"""
        return not self._status.is_completed() and not self._status.is_cancelled()
```

### Step 2: Create Repository Interface

**File: `Backend/bookings/domain/repositories.py`**

```python
"""
Repository interfaces for Bookings domain
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from shared.domain.value_objects import ReservationId, UserId, DestinationId
from .reservation import Reservation


class IReservationRepository(ABC):
    """Repository interface for Reservation aggregate"""
    
    @abstractmethod
    def get_by_id(self, reservation_id: ReservationId) -> Optional[Reservation]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: UserId) -> List[Reservation]:
        pass
    
    @abstractmethod
    def get_by_destination(self, destination_id: DestinationId) -> List[Reservation]:
        pass
    
    @abstractmethod
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Reservation]:
        pass
    
    @abstractmethod
    def save(self, reservation: Reservation) -> None:
        pass
    
    @abstractmethod
    def delete(self, reservation: Reservation) -> None:
        pass
    
    @abstractmethod
    def exists(self, reservation_id: ReservationId) -> bool:
        pass
```

### Step 3: Create Infrastructure Layer

**File: `Backend/bookings/infrastructure/__init__.py`**
```python
"""
Infrastructure layer for Bookings
"""
```

**File: `Backend/bookings/infrastructure/django_repositories.py`**

```python
"""
Django ORM implementation of booking repositories
"""
from typing import List, Optional
from datetime import date
from decimal import Decimal
from shared.domain.value_objects import ReservationId, UserId, DestinationId, Money
from shared.infrastructure.event_bus import get_event_bus
from ..models import Booking as BookingModel
from ..domain.repositories import IReservationRepository
from ..domain.reservation import Reservation, BookingStatus


class DjangoReservationRepository(IReservationRepository):
    """Django ORM implementation of reservation repository"""
    
    def __init__(self):
        self._event_bus = get_event_bus()
    
    def get_by_id(self, reservation_id: ReservationId) -> Optional[Reservation]:
        try:
            model = BookingModel.objects.get(id=reservation_id.value)
            return self._to_domain(model)
        except BookingModel.DoesNotExist:
            return None
    
    def get_by_user(self, user_id: UserId) -> List[Reservation]:
        models = BookingModel.objects.filter(user_id=user_id.value)
        return [self._to_domain(model) for model in models]
    
    def get_by_destination(self, destination_id: DestinationId) -> List[Reservation]:
        models = BookingModel.objects.filter(tourist_site_id=destination_id.value)
        return [self._to_domain(model) for model in models]
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Reservation]:
        models = BookingModel.objects.filter(
            booking_date__gte=start_date,
            booking_date__lte=end_date
        )
        return [self._to_domain(model) for model in models]
    
    def save(self, reservation: Reservation) -> None:
        model = self._to_model(reservation)
        model.save()
        
        # Publish domain events
        for event in reservation.domain_events:
            self._event_bus.publish(event)
        reservation.clear_domain_events()
    
    def delete(self, reservation: Reservation) -> None:
        try:
            model = BookingModel.objects.get(id=reservation.id.value)
            model.delete()
        except BookingModel.DoesNotExist:
            pass
    
    def exists(self, reservation_id: ReservationId) -> bool:
        return BookingModel.objects.filter(id=reservation_id.value).exists()
    
    def _to_domain(self, model: BookingModel) -> Reservation:
        """Convert Django model to domain aggregate"""
        return Reservation(
            id=ReservationId(model.id),
            user_id=UserId(model.user_id),
            destination_id=DestinationId(model.tourist_site_id),
            booking_date=model.booking_date,
            number_of_visitors=model.number_of_visitors,
            total_price=Money(model.total_price, 'XAF'),
            status=BookingStatus(model.status),
            special_requests=model.special_requests or ""
        )
    
    def _to_model(self, reservation: Reservation) -> BookingModel:
        """Convert domain aggregate to Django model"""
        try:
            model = BookingModel.objects.get(id=reservation.id.value)
        except BookingModel.DoesNotExist:
            model = BookingModel(id=reservation.id.value)
        
        model.user_id = reservation.user_id.value
        model.tourist_site_id = reservation.destination_id.value
        model.booking_date = reservation.booking_date
        model.number_of_visitors = reservation.number_of_visitors
        model.total_price = reservation.total_price.amount
        model.status = reservation.status.value
        model.special_requests = reservation.special_requests
        
        return model


# Singleton instance
_reservation_repository = None


def get_reservation_repository() -> IReservationRepository:
    """Get the reservation repository instance"""
    global _reservation_repository
    if _reservation_repository is None:
        _reservation_repository = DjangoReservationRepository()
    return _reservation_repository
```

### Step 4: Create Application Layer

Follow the same pattern as Tourism:
- Create `bookings/application/commands.py` with CreateReservationCommand, ConfirmReservationCommand, etc.
- Create `bookings/application/queries.py` with GetReservationQuery, GetUserReservationsQuery, etc.
- Create `bookings/application/services.py` with BookingApplicationService

### Step 5: Create Views and URLs

Follow the same pattern as Tourism:
- Create `bookings/views_ddd.py` with DDD-based views
- Create `bookings/urls_ddd.py` with URL routing
- Update `natourcam/urls.py` to include bookings DDD routes

## Extending to Accounts Context

### Domain Layer

**File: `Backend/accounts/domain/user.py`**

```python
"""
User aggregate root - Manages user identity and profile
"""
from shared.domain.base import AggregateRoot, DomainEvent, DomainException
from shared.domain.value_objects import UserId, Email, PhoneNumber


class UserRegistered(DomainEvent):
    def __init__(self, user_id: UserId, email: Email):
        super().__init__()
        self.user_id = user_id
        self.email = email


class UserVerified(DomainEvent):
    def __init__(self, user_id: UserId):
        super().__init__()
        self.user_id = user_id


class User(AggregateRoot):
    """
    User aggregate root.
    Manages user identity, authentication, and profile.
    """
    
    def __init__(
        self,
        id: UserId,
        email: Email,
        username: str,
        phone_number: Optional[PhoneNumber] = None,
        language: str = 'en',
        is_verified: bool = False
    ):
        super().__init__(id)
        self._email = email
        self._username = username
        self._phone_number = phone_number
        self._language = language
        self._is_verified = is_verified
        
        self._validate()
    
    @classmethod
    def register(
        cls,
        id: UserId,
        email: Email,
        username: str,
        phone_number: Optional[PhoneNumber] = None
    ) -> 'User':
        """Factory method to register a new user"""
        user = cls(
            id=id,
            email=email,
            username=username,
            phone_number=phone_number,
            is_verified=False
        )
        
        user.add_domain_event(UserRegistered(id, email))
        
        return user
    
    def _validate(self):
        """Validate user invariants"""
        if not self._username or len(self._username) < 3:
            raise DomainException("Username must be at least 3 characters")
        
        if self._language not in ['en', 'fr']:
            raise DomainException("Language must be 'en' or 'fr'")
    
    # Properties
    @property
    def email(self) -> Email:
        return self._email
    
    @property
    def username(self) -> str:
        return self._username
    
    @property
    def phone_number(self) -> Optional[PhoneNumber]:
        return self._phone_number
    
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def is_verified(self) -> bool:
        return self._is_verified
    
    # Business methods
    def verify(self):
        """Verify the user"""
        if self._is_verified:
            return  # Already verified
        
        self._is_verified = True
        self.add_domain_event(UserVerified(self.id))
    
    def update_profile(
        self,
        phone_number: Optional[PhoneNumber] = None,
        language: Optional[str] = None
    ):
        """Update user profile"""
        if phone_number:
            self._phone_number = phone_number
        if language:
            if language not in ['en', 'fr']:
                raise DomainException("Language must be 'en' or 'fr'")
            self._language = language
    
    def can_make_booking(self) -> bool:
        """Check if user can make bookings"""
        return self._is_verified
```

## Quick Implementation Checklist

For each context (Bookings, Accounts):

### Domain Layer
- [ ] Create `domain/__init__.py`
- [ ] Create aggregate root (e.g., `reservation.py`, `user.py`)
- [ ] Define domain events
- [ ] Define value objects
- [ ] Create `repositories.py` with interfaces

### Infrastructure Layer
- [ ] Create `infrastructure/__init__.py`
- [ ] Create `django_repositories.py`
- [ ] Implement repository with `_to_domain()` and `_to_model()` methods
- [ ] Add singleton getter function

### Application Layer
- [ ] Create `application/__init__.py`
- [ ] Create `commands.py` with command DTOs and handlers
- [ ] Create `queries.py` with query DTOs and handlers
- [ ] Create `services.py` with application service facade

### Presentation Layer
- [ ] Create `views_ddd.py` with DDD-based views
- [ ] Create `urls_ddd.py` with URL routing
- [ ] Update `natourcam/urls.py` to include new routes

## Testing Template

```python
# Test domain logic
def test_reservation_confirmation():
    reservation = Reservation.create(...)
    reservation.confirm()
    assert reservation.status.is_confirmed()
    assert len(reservation.domain_events) == 2  # Created + Confirmed

# Test application service
def test_create_reservation():
    service = get_booking_service()
    command = CreateReservationCommand(...)
    reservation_id = service.create_reservation(command)
    assert reservation_id is not None
```

## Summary

The Tourism context provides a complete, working template. To extend to other contexts:

1. **Copy the structure** from Tourism
2. **Adapt the domain model** to the specific context
3. **Implement repositories** to adapt Django ORM
4. **Create application services** for use cases
5. **Add views and URLs** for API endpoints

All contexts follow the same pattern, making it easy to replicate and maintain consistency across the codebase.
