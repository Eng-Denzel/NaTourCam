"""
Command handlers for Tourism - Write operations
Commands represent intentions to change state
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import time
from shared.domain.value_objects import DestinationId, RegionId, Location, Money
from ..domain.repositories import IDestinationRepository, IRegionRepository
from ..domain.destination import TouristDestination, InvalidDestinationDataError
from ..domain.region import Region, InvalidRegionDataError


# Commands (DTOs)
@dataclass
class CreateDestinationCommand:
    """Command to create a new destination"""
    name: str
    description: str
    region_id: int
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    address: Optional[str] = None
    entrance_fee: Optional[Decimal] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None


@dataclass
class UpdateDestinationCommand:
    """Command to update a destination"""
    destination_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    address: Optional[str] = None
    entrance_fee: Optional[Decimal] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None


@dataclass
class ActivateDestinationCommand:
    """Command to activate a destination"""
    destination_id: int


@dataclass
class DeactivateDestinationCommand:
    """Command to deactivate a destination"""
    destination_id: int


@dataclass
class CreateRegionCommand:
    """Command to create a new region"""
    name: str
    code: str
    description: str = ""


@dataclass
class UpdateRegionCommand:
    """Command to update a region"""
    region_id: int
    name: Optional[str] = None
    description: Optional[str] = None


# Command Handlers
class CreateDestinationHandler:
    """Handler for creating a new destination"""
    
    def __init__(self, destination_repo: IDestinationRepository, region_repo: IRegionRepository):
        self._destination_repo = destination_repo
        self._region_repo = region_repo
    
    def handle(self, command: CreateDestinationCommand) -> DestinationId:
        """Execute the command"""
        # Validate region exists
        region_id = RegionId(command.region_id)
        if not self._region_repo.exists(region_id):
            raise InvalidDestinationDataError(f"Region with ID {command.region_id} does not exist")
        
        # Create location if coordinates provided
        location = None
        if command.latitude and command.longitude:
            location = Location(
                latitude=command.latitude,
                longitude=command.longitude,
                address=command.address
            )
        
        # Create entrance fee
        entrance_fee = None
        if command.entrance_fee:
            entrance_fee = Money(command.entrance_fee, 'XAF')
        
        # Generate new ID (in real app, this might come from database sequence)
        # For now, we'll let Django handle it
        from ..models import TouristSite as TouristSiteModel
        next_id = (TouristSiteModel.objects.order_by('-id').first().id + 1) if TouristSiteModel.objects.exists() else 1
        destination_id = DestinationId(next_id)
        
        # Create destination aggregate
        destination = TouristDestination.create(
            id=destination_id,
            name=command.name,
            description=command.description,
            region_id=region_id,
            location=location,
            entrance_fee=entrance_fee,
            opening_time=command.opening_time,
            closing_time=command.closing_time
        )
        
        # Save
        self._destination_repo.save(destination)
        
        return destination_id


class UpdateDestinationHandler:
    """Handler for updating a destination"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, command: UpdateDestinationCommand) -> None:
        """Execute the command"""
        destination_id = DestinationId(command.destination_id)
        destination = self._destination_repo.get_by_id(destination_id)
        
        if not destination:
            raise InvalidDestinationDataError(f"Destination with ID {command.destination_id} not found")
        
        # Create location if coordinates provided
        location = None
        if command.latitude and command.longitude:
            location = Location(
                latitude=command.latitude,
                longitude=command.longitude,
                address=command.address
            )
        
        # Create entrance fee if provided
        entrance_fee = None
        if command.entrance_fee is not None:
            entrance_fee = Money(command.entrance_fee, 'XAF')
        
        # Update destination
        destination.update_details(
            name=command.name,
            description=command.description,
            location=location,
            entrance_fee=entrance_fee,
            opening_time=command.opening_time,
            closing_time=command.closing_time
        )
        
        # Save
        self._destination_repo.save(destination)


class ActivateDestinationHandler:
    """Handler for activating a destination"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, command: ActivateDestinationCommand) -> None:
        """Execute the command"""
        destination_id = DestinationId(command.destination_id)
        destination = self._destination_repo.get_by_id(destination_id)
        
        if not destination:
            raise InvalidDestinationDataError(f"Destination with ID {command.destination_id} not found")
        
        destination.activate()
        self._destination_repo.save(destination)


class DeactivateDestinationHandler:
    """Handler for deactivating a destination"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, command: DeactivateDestinationCommand) -> None:
        """Execute the command"""
        destination_id = DestinationId(command.destination_id)
        destination = self._destination_repo.get_by_id(destination_id)
        
        if not destination:
            raise InvalidDestinationDataError(f"Destination with ID {command.destination_id} not found")
        
        destination.deactivate()
        self._destination_repo.save(destination)


class CreateRegionHandler:
    """Handler for creating a new region"""
    
    def __init__(self, region_repo: IRegionRepository):
        self._region_repo = region_repo
    
    def handle(self, command: CreateRegionCommand) -> RegionId:
        """Execute the command"""
        # Check if code already exists
        existing = self._region_repo.get_by_code(command.code)
        if existing:
            raise InvalidRegionDataError(f"Region with code {command.code} already exists")
        
        # Generate new ID
        from ..models import Region as RegionModel
        next_id = (RegionModel.objects.order_by('-id').first().id + 1) if RegionModel.objects.exists() else 1
        region_id = RegionId(next_id)
        
        # Create region aggregate
        region = Region.create(
            id=region_id,
            name=command.name,
            code=command.code,
            description=command.description
        )
        
        # Save
        self._region_repo.save(region)
        
        return region_id


class UpdateRegionHandler:
    """Handler for updating a region"""
    
    def __init__(self, region_repo: IRegionRepository):
        self._region_repo = region_repo
    
    def handle(self, command: UpdateRegionCommand) -> None:
        """Execute the command"""
        region_id = RegionId(command.region_id)
        region = self._region_repo.get_by_id(region_id)
        
        if not region:
            raise InvalidRegionDataError(f"Region with ID {command.region_id} not found")
        
        # Update region
        region.update_details(
            name=command.name,
            description=command.description
        )
        
        # Save
        self._region_repo.save(region)
