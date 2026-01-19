"""
Base classes for domain-driven design building blocks
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any, Optional
from uuid import UUID, uuid4


class DomainEvent:
    """Base class for all domain events"""
    
    def __init__(self):
        self.occurred_at = datetime.utcnow()
        self.event_id = uuid4()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(event_id={self.event_id}, occurred_at={self.occurred_at})"


class Entity(ABC):
    """
    Base class for entities.
    Entities have identity and lifecycle.
    """
    
    def __init__(self, id: Any):
        self._id = id
    
    @property
    def id(self) -> Any:
        return self._id
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class AggregateRoot(Entity):
    """
    Base class for aggregate roots.
    Aggregate roots are entities that serve as entry points to aggregates.
    They maintain consistency boundaries and emit domain events.
    """
    
    def __init__(self, id: Any):
        super().__init__(id)
        self._domain_events: List[DomainEvent] = []
    
    def add_domain_event(self, event: DomainEvent):
        """Add a domain event to be published"""
        self._domain_events.append(event)
    
    @property
    def domain_events(self) -> List[DomainEvent]:
        """Get all domain events"""
        return self._domain_events.copy()
    
    def clear_domain_events(self):
        """Clear all domain events after they've been published"""
        self._domain_events.clear()


class ValueObject(ABC):
    """
    Base class for value objects.
    Value objects are immutable and defined by their attributes.
    """
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __repr__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class IRepository(ABC):
    """
    Base interface for repositories.
    Repositories provide collection-like interface for aggregates.
    """
    
    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[AggregateRoot]:
        """Retrieve an aggregate by its ID"""
        pass
    
    @abstractmethod
    def save(self, aggregate: AggregateRoot) -> None:
        """Save an aggregate"""
        pass
    
    @abstractmethod
    def delete(self, aggregate: AggregateRoot) -> None:
        """Delete an aggregate"""
        pass


class DomainService(ABC):
    """
    Base class for domain services.
    Domain services contain domain logic that doesn't naturally fit within entities or value objects.
    """
    pass


class IEventBus(ABC):
    """Interface for event bus to publish domain events"""
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event"""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: type, handler: callable) -> None:
        """Subscribe a handler to an event type"""
        pass


class DomainException(Exception):
    """Base class for domain exceptions"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
