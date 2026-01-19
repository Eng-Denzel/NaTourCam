"""
Django ORM implementation of repository interfaces
These adapt Django models to domain aggregates
"""
from typing import List, Optional
from decimal import Decimal
from django.db.models import Q
from shared.domain.value_objects import DestinationId, RegionId, Location, Money
from shared.infrastructure.event_bus import get_event_bus
from ..models import TouristSite as TouristSiteModel, Region as RegionModel
from ..domain.repositories import IDestinationRepository, IRegionRepository
from ..domain.destination import TouristDestination
from ..domain.region import Region


class DjangoDestinationRepository(IDestinationRepository):
    """Django ORM implementation of destination repository"""
    
    def __init__(self):
        self._event_bus = get_event_bus()
    
    def get_by_id(self, destination_id: DestinationId) -> Optional[TouristDestination]:
        """Retrieve a destination by its ID"""
        try:
            model = TouristSiteModel.objects.get(id=destination_id.value)
            return self._to_domain(model)
        except TouristSiteModel.DoesNotExist:
            return None
    
    def get_all_active(self) -> List[TouristDestination]:
        """Retrieve all active destinations"""
        models = TouristSiteModel.objects.filter(is_active=True)
        return [self._to_domain(model) for model in models]
    
    def get_by_region(self, region_id: RegionId) -> List[TouristDestination]:
        """Retrieve all destinations in a specific region"""
        models = TouristSiteModel.objects.filter(region_id=region_id.value)
        return [self._to_domain(model) for model in models]
    
    def search(self, query: str) -> List[TouristDestination]:
        """Search destinations by name or description"""
        models = TouristSiteModel.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return [self._to_domain(model) for model in models]
    
    def save(self, destination: TouristDestination) -> None:
        """Save a destination (create or update)"""
        # Convert domain model to Django model
        model = self._to_model(destination)
        model.save()
        
        # Publish domain events
        for event in destination.domain_events:
            self._event_bus.publish(event)
        destination.clear_domain_events()
    
    def delete(self, destination: TouristDestination) -> None:
        """Delete a destination"""
        try:
            model = TouristSiteModel.objects.get(id=destination.id.value)
            model.delete()
        except TouristSiteModel.DoesNotExist:
            pass
    
    def exists(self, destination_id: DestinationId) -> bool:
        """Check if a destination exists"""
        return TouristSiteModel.objects.filter(id=destination_id.value).exists()
    
    def _to_domain(self, model: TouristSiteModel) -> TouristDestination:
        """Convert Django model to domain aggregate"""
        location = None
        if model.latitude and model.longitude:
            location = Location(
                latitude=model.latitude,
                longitude=model.longitude,
                address=model.address or None
            )
        
        entrance_fee = None
        if model.entrance_fee:
            entrance_fee = Money(model.entrance_fee, 'XAF')
        
        destination = TouristDestination(
            id=DestinationId(model.id),
            name=model.name,
            description=model.description,
            region_id=RegionId(model.region_id),
            location=location,
            entrance_fee=entrance_fee,
            opening_time=model.opening_time,
            closing_time=model.closing_time,
            is_active=model.is_active
        )
        
        # Add images
        for image in model.images.all():
            destination.add_image(image.image.name)
        
        return destination
    
    def _to_model(self, destination: TouristDestination) -> TouristSiteModel:
        """Convert domain aggregate to Django model"""
        try:
            model = TouristSiteModel.objects.get(id=destination.id.value)
        except TouristSiteModel.DoesNotExist:
            model = TouristSiteModel(id=destination.id.value)
        
        model.name = destination.name
        model.description = destination.description
        model.region_id = destination.region_id.value
        model.is_active = destination.is_active
        
        if destination.location:
            model.latitude = destination.location.latitude
            model.longitude = destination.location.longitude
            model.address = destination.location.address or ""
        
        if destination.entrance_fee:
            model.entrance_fee = destination.entrance_fee.amount
        
        model.opening_time = destination.opening_time
        model.closing_time = destination.closing_time
        
        return model


class DjangoRegionRepository(IRegionRepository):
    """Django ORM implementation of region repository"""
    
    def __init__(self):
        self._event_bus = get_event_bus()
    
    def get_by_id(self, region_id: RegionId) -> Optional[Region]:
        """Retrieve a region by its ID"""
        try:
            model = RegionModel.objects.get(id=region_id.value)
            return self._to_domain(model)
        except RegionModel.DoesNotExist:
            return None
    
    def get_by_code(self, code: str) -> Optional[Region]:
        """Retrieve a region by its code"""
        try:
            model = RegionModel.objects.get(code=code.upper())
            return self._to_domain(model)
        except RegionModel.DoesNotExist:
            return None
    
    def get_all(self) -> List[Region]:
        """Retrieve all regions"""
        models = RegionModel.objects.all()
        return [self._to_domain(model) for model in models]
    
    def save(self, region: Region) -> None:
        """Save a region (create or update)"""
        model = self._to_model(region)
        model.save()
        
        # Publish domain events
        for event in region.domain_events:
            self._event_bus.publish(event)
        region.clear_domain_events()
    
    def delete(self, region: Region) -> None:
        """Delete a region"""
        try:
            model = RegionModel.objects.get(id=region.id.value)
            model.delete()
        except RegionModel.DoesNotExist:
            pass
    
    def exists(self, region_id: RegionId) -> bool:
        """Check if a region exists"""
        return RegionModel.objects.filter(id=region_id.value).exists()
    
    def _to_domain(self, model: RegionModel) -> Region:
        """Convert Django model to domain aggregate"""
        return Region(
            id=RegionId(model.id),
            name=model.name,
            code=model.code,
            description=model.description or ""
        )
    
    def _to_model(self, region: Region) -> RegionModel:
        """Convert domain aggregate to Django model"""
        try:
            model = RegionModel.objects.get(id=region.id.value)
        except RegionModel.DoesNotExist:
            model = RegionModel(id=region.id.value)
        
        model.name = region.name
        model.code = region.code
        model.description = region.description
        
        return model


# Singleton instances
_destination_repository = None
_region_repository = None


def get_destination_repository() -> IDestinationRepository:
    """Get the destination repository instance"""
    global _destination_repository
    if _destination_repository is None:
        _destination_repository = DjangoDestinationRepository()
    return _destination_repository


def get_region_repository() -> IRegionRepository:
    """Get the region repository instance"""
    global _region_repository
    if _region_repository is None:
        _region_repository = DjangoRegionRepository()
    return _region_repository
