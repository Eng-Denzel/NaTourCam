"""
Query handlers for Tourism - Read operations
Queries return data without modifying state
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from shared.domain.value_objects import DestinationId, RegionId
from ..domain.repositories import IDestinationRepository, IRegionRepository
from ..domain.destination import TouristDestination
from ..domain.region import Region


# Query DTOs
@dataclass
class GetDestinationQuery:
    """Query to get a single destination"""
    destination_id: int


@dataclass
class GetAllDestinationsQuery:
    """Query to get all active destinations"""
    pass


@dataclass
class GetDestinationsByRegionQuery:
    """Query to get destinations by region"""
    region_id: int


@dataclass
class SearchDestinationsQuery:
    """Query to search destinations"""
    query: str


@dataclass
class GetRegionQuery:
    """Query to get a single region"""
    region_id: int


@dataclass
class GetAllRegionsQuery:
    """Query to get all regions"""
    pass


# Query Result DTOs
@dataclass
class DestinationDTO:
    """Data transfer object for destination"""
    id: int
    name: str
    description: str
    region_id: int
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    entrance_fee: float
    currency: str
    opening_time: Optional[str]
    closing_time: Optional[str]
    is_active: bool
    is_free: bool
    is_open_24_hours: bool
    images: List[str]


@dataclass
class RegionDTO:
    """Data transfer object for region"""
    id: int
    name: str
    code: str
    description: str


# Query Handlers
class GetDestinationHandler:
    """Handler for getting a single destination"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, query: GetDestinationQuery) -> Optional[DestinationDTO]:
        """Execute the query"""
        destination = self._destination_repo.get_by_id(DestinationId(query.destination_id))
        if not destination:
            return None
        return self._to_dto(destination)
    
    def _to_dto(self, destination: TouristDestination) -> DestinationDTO:
        """Convert domain model to DTO"""
        return DestinationDTO(
            id=destination.id.value,
            name=destination.name,
            description=destination.description,
            region_id=destination.region_id.value,
            latitude=float(destination.location.latitude) if destination.location else None,
            longitude=float(destination.location.longitude) if destination.location else None,
            address=destination.location.address if destination.location else None,
            entrance_fee=float(destination.entrance_fee.amount),
            currency=destination.entrance_fee.currency,
            opening_time=str(destination.opening_time) if destination.opening_time else None,
            closing_time=str(destination.closing_time) if destination.closing_time else None,
            is_active=destination.is_active,
            is_free=destination.is_free_admission(),
            is_open_24_hours=destination.is_open_24_hours(),
            images=destination.images
        )


class GetAllDestinationsHandler:
    """Handler for getting all active destinations"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, query: GetAllDestinationsQuery) -> List[DestinationDTO]:
        """Execute the query"""
        destinations = self._destination_repo.get_all_active()
        return [self._to_dto(d) for d in destinations]
    
    def _to_dto(self, destination: TouristDestination) -> DestinationDTO:
        """Convert domain model to DTO"""
        return DestinationDTO(
            id=destination.id.value,
            name=destination.name,
            description=destination.description,
            region_id=destination.region_id.value,
            latitude=float(destination.location.latitude) if destination.location else None,
            longitude=float(destination.location.longitude) if destination.location else None,
            address=destination.location.address if destination.location else None,
            entrance_fee=float(destination.entrance_fee.amount),
            currency=destination.entrance_fee.currency,
            opening_time=str(destination.opening_time) if destination.opening_time else None,
            closing_time=str(destination.closing_time) if destination.closing_time else None,
            is_active=destination.is_active,
            is_free=destination.is_free_admission(),
            is_open_24_hours=destination.is_open_24_hours(),
            images=destination.images
        )


class GetDestinationsByRegionHandler:
    """Handler for getting destinations by region"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, query: GetDestinationsByRegionQuery) -> List[DestinationDTO]:
        """Execute the query"""
        destinations = self._destination_repo.get_by_region(RegionId(query.region_id))
        return [self._to_dto(d) for d in destinations]
    
    def _to_dto(self, destination: TouristDestination) -> DestinationDTO:
        """Convert domain model to DTO"""
        return DestinationDTO(
            id=destination.id.value,
            name=destination.name,
            description=destination.description,
            region_id=destination.region_id.value,
            latitude=float(destination.location.latitude) if destination.location else None,
            longitude=float(destination.location.longitude) if destination.location else None,
            address=destination.location.address if destination.location else None,
            entrance_fee=float(destination.entrance_fee.amount),
            currency=destination.entrance_fee.currency,
            opening_time=str(destination.opening_time) if destination.opening_time else None,
            closing_time=str(destination.closing_time) if destination.closing_time else None,
            is_active=destination.is_active,
            is_free=destination.is_free_admission(),
            is_open_24_hours=destination.is_open_24_hours(),
            images=destination.images
        )


class SearchDestinationsHandler:
    """Handler for searching destinations"""
    
    def __init__(self, destination_repo: IDestinationRepository):
        self._destination_repo = destination_repo
    
    def handle(self, query: SearchDestinationsQuery) -> List[DestinationDTO]:
        """Execute the query"""
        destinations = self._destination_repo.search(query.query)
        return [self._to_dto(d) for d in destinations]
    
    def _to_dto(self, destination: TouristDestination) -> DestinationDTO:
        """Convert domain model to DTO"""
        return DestinationDTO(
            id=destination.id.value,
            name=destination.name,
            description=destination.description,
            region_id=destination.region_id.value,
            latitude=float(destination.location.latitude) if destination.location else None,
            longitude=float(destination.location.longitude) if destination.location else None,
            address=destination.location.address if destination.location else None,
            entrance_fee=float(destination.entrance_fee.amount),
            currency=destination.entrance_fee.currency,
            opening_time=str(destination.opening_time) if destination.opening_time else None,
            closing_time=str(destination.closing_time) if destination.closing_time else None,
            is_active=destination.is_active,
            is_free=destination.is_free_admission(),
            is_open_24_hours=destination.is_open_24_hours(),
            images=destination.images
        )


class GetRegionHandler:
    """Handler for getting a single region"""
    
    def __init__(self, region_repo: IRegionRepository):
        self._region_repo = region_repo
    
    def handle(self, query: GetRegionQuery) -> Optional[RegionDTO]:
        """Execute the query"""
        region = self._region_repo.get_by_id(RegionId(query.region_id))
        if not region:
            return None
        return self._to_dto(region)
    
    def _to_dto(self, region: Region) -> RegionDTO:
        """Convert domain model to DTO"""
        return RegionDTO(
            id=region.id.value,
            name=region.name,
            code=region.code,
            description=region.description
        )


class GetAllRegionsHandler:
    """Handler for getting all regions"""
    
    def __init__(self, region_repo: IRegionRepository):
        self._region_repo = region_repo
    
    def handle(self, query: GetAllRegionsQuery) -> List[RegionDTO]:
        """Execute the query"""
        regions = self._region_repo.get_all()
        return [self._to_dto(r) for r in regions]
    
    def _to_dto(self, region: Region) -> RegionDTO:
        """Convert domain model to DTO"""
        return RegionDTO(
            id=region.id.value,
            name=region.name,
            code=region.code,
            description=region.description
        )
