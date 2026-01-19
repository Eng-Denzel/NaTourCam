"""
TouristDestination aggregate root - Rich domain model with business logic
"""
from typing import List, Optional
from datetime import time
from decimal import Decimal
from shared.domain.base import AggregateRoot, DomainEvent, DomainException
from shared.domain.value_objects import DestinationId, RegionId, Location, Money


class DestinationNotActiveError(DomainException):
    """Raised when trying to perform operations on inactive destination"""
    pass


class InvalidDestinationDataError(DomainException):
    """Raised when destination data is invalid"""
    pass


# Domain Events
class DestinationCreated(DomainEvent):
    """Event raised when a new destination is created"""
    def __init__(self, destination_id: DestinationId, name: str, region_id: RegionId):
        super().__init__()
        self.destination_id = destination_id
        self.name = name
        self.region_id = region_id


class DestinationActivated(DomainEvent):
    """Event raised when a destination is activated"""
    def __init__(self, destination_id: DestinationId):
        super().__init__()
        self.destination_id = destination_id


class DestinationDeactivated(DomainEvent):
    """Event raised when a destination is deactivated"""
    def __init__(self, destination_id: DestinationId):
        super().__init__()
        self.destination_id = destination_id


class DestinationUpdated(DomainEvent):
    """Event raised when destination details are updated"""
    def __init__(self, destination_id: DestinationId):
        super().__init__()
        self.destination_id = destination_id


class TouristDestination(AggregateRoot):
    """
    TouristDestination aggregate root.
    Represents a tourist destination with all its business rules.
    """
    
    def __init__(
        self,
        id: DestinationId,
        name: str,
        description: str,
        region_id: RegionId,
        location: Optional[Location] = None,
        entrance_fee: Optional[Money] = None,
        opening_time: Optional[time] = None,
        closing_time: Optional[time] = None,
        is_active: bool = True
    ):
        super().__init__(id)
        self._name = name
        self._description = description
        self._region_id = region_id
        self._location = location
        self._entrance_fee = entrance_fee or Money(Decimal('0'), 'XAF')
        self._opening_time = opening_time
        self._closing_time = closing_time
        self._is_active = is_active
        self._images: List[str] = []
        
        # Validate
        self._validate()
    
    @classmethod
    def create(
        cls,
        id: DestinationId,
        name: str,
        description: str,
        region_id: RegionId,
        location: Optional[Location] = None,
        entrance_fee: Optional[Money] = None,
        opening_time: Optional[time] = None,
        closing_time: Optional[time] = None
    ) -> 'TouristDestination':
        """Factory method to create a new destination"""
        destination = cls(
            id=id,
            name=name,
            description=description,
            region_id=region_id,
            location=location,
            entrance_fee=entrance_fee,
            opening_time=opening_time,
            closing_time=closing_time,
            is_active=True
        )
        
        # Raise domain event
        destination.add_domain_event(
            DestinationCreated(id, name, region_id)
        )
        
        return destination
    
    def _validate(self):
        """Validate destination invariants"""
        if not self._name or len(self._name) < 3:
            raise InvalidDestinationDataError("Destination name must be at least 3 characters")
        
        if not self._description:
            raise InvalidDestinationDataError("Destination must have a description")
        
        if self._opening_time and self._closing_time:
            if self._opening_time >= self._closing_time:
                raise InvalidDestinationDataError(
                    "Opening time must be before closing time"
                )
    
    # Properties
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def region_id(self) -> RegionId:
        return self._region_id
    
    @property
    def location(self) -> Optional[Location]:
        return self._location
    
    @property
    def entrance_fee(self) -> Money:
        return self._entrance_fee
    
    @property
    def opening_time(self) -> Optional[time]:
        return self._opening_time
    
    @property
    def closing_time(self) -> Optional[time]:
        return self._closing_time
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def images(self) -> List[str]:
        return self._images.copy()
    
    # Business methods
    def update_details(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[Location] = None,
        entrance_fee: Optional[Money] = None,
        opening_time: Optional[time] = None,
        closing_time: Optional[time] = None
    ):
        """Update destination details"""
        if name:
            self._name = name
        if description:
            self._description = description
        if location:
            self._location = location
        if entrance_fee:
            self._entrance_fee = entrance_fee
        if opening_time is not None:
            self._opening_time = opening_time
        if closing_time is not None:
            self._closing_time = closing_time
        
        self._validate()
        self.add_domain_event(DestinationUpdated(self.id))
    
    def activate(self):
        """Activate the destination"""
        if self._is_active:
            return  # Already active
        
        self._is_active = True
        self.add_domain_event(DestinationActivated(self.id))
    
    def deactivate(self):
        """Deactivate the destination"""
        if not self._is_active:
            return  # Already inactive
        
        self._is_active = False
        self.add_domain_event(DestinationDeactivated(self.id))
    
    def add_image(self, image_path: str):
        """Add an image to the destination"""
        if not image_path:
            raise InvalidDestinationDataError("Image path cannot be empty")
        
        if image_path not in self._images:
            self._images.append(image_path)
    
    def remove_image(self, image_path: str):
        """Remove an image from the destination"""
        if image_path in self._images:
            self._images.remove(image_path)
    
    def is_free_admission(self) -> bool:
        """Check if the destination has free admission"""
        return self._entrance_fee.is_zero()
    
    def is_open_24_hours(self) -> bool:
        """Check if the destination is open 24 hours"""
        return self._opening_time is None and self._closing_time is None
    
    def is_open_at(self, check_time: time) -> bool:
        """Check if the destination is open at a specific time"""
        if not self._is_active:
            return False
        
        if self.is_open_24_hours():
            return True
        
        if not self._opening_time or not self._closing_time:
            return False
        
        return self._opening_time <= check_time <= self._closing_time
    
    def can_be_booked(self) -> bool:
        """Check if the destination can be booked"""
        return self._is_active
    
    def __repr__(self):
        return f"TouristDestination(id={self.id}, name='{self._name}', active={self._is_active})"
