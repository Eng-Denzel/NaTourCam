"""
Event bus implementation for publishing and subscribing to domain events
"""
from typing import Dict, List, Callable, Type
import logging
from ..domain.base import IEventBus, DomainEvent


logger = logging.getLogger(__name__)


class InMemoryEventBus(IEventBus):
    """
    Simple in-memory event bus implementation.
    For production, consider using a message broker like RabbitMQ or Kafka.
    """
    
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}
    
    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event to all subscribed handlers"""
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])
        
        logger.info(f"Publishing event: {event}")
        
        for handler in handlers:
            try:
                handler(event)
                logger.debug(f"Handler {handler.__name__} processed {event_type.__name__}")
            except Exception as e:
                logger.error(
                    f"Error in handler {handler.__name__} for event {event_type.__name__}: {e}",
                    exc_info=True
                )
                # Continue processing other handlers even if one fails
    
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Subscribe a handler to an event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append(handler)
        logger.info(f"Subscribed {handler.__name__} to {event_type.__name__}")
    
    def clear_handlers(self):
        """Clear all handlers (useful for testing)"""
        self._handlers.clear()


# Global event bus instance
_event_bus = InMemoryEventBus()


def get_event_bus() -> IEventBus:
    """Get the global event bus instance"""
    return _event_bus
