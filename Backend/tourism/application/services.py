"""
Application services for Tourism - Facade for use cases
These services coordinate commands and queries
"""
from typing import List, Optional
from .commands import (
    CreateDestinationCommand, UpdateDestinationCommand,
    ActivateDestinationCommand, DeactivateDestinationCommand,
    CreateRegionCommand, UpdateRegionCommand,
    CreateDestinationHandler, UpdateDestinationHandler,
    ActivateDestinationHandler, DeactivateDestinationHandler,
    CreateRegionHandler, UpdateRegionHandler
)
from .queries import (
    GetDestinationQuery, GetAllDestinationsQuery,
    GetDestinationsByRegionQuery, SearchDestinationsQuery,
    GetRegionQuery, GetAllRegionsQuery,
    GetDestinationHandler, GetAllDestinationsHandler,
    GetDestinationsByRegionHandler, SearchDestinationsHandler,
    GetRegionHandler, GetAllRegionsHandler,
    DestinationDTO, RegionDTO
)
from ..infrastructure.django_repositories import get_destination_repository, get_region_repository


class TourismApplicationService:
    """
    Application service for Tourism bounded context.
    This is the main entry point for all tourism-related operations.
    """
    
    def __init__(self):
        self._destination_repo = get_destination_repository()
        self._region_repo = get_region_repository()
    
    # Destination Commands
    def create_destination(self, command: CreateDestinationCommand) -> int:
        """Create a new destination"""
        handler = CreateDestinationHandler(self._destination_repo, self._region_repo)
        destination_id = handler.handle(command)
        return destination_id.value
    
    def update_destination(self, command: UpdateDestinationCommand) -> None:
        """Update a destination"""
        handler = UpdateDestinationHandler(self._destination_repo)
        handler.handle(command)
    
    def activate_destination(self, destination_id: int) -> None:
        """Activate a destination"""
        command = ActivateDestinationCommand(destination_id=destination_id)
        handler = ActivateDestinationHandler(self._destination_repo)
        handler.handle(command)
    
    def deactivate_destination(self, destination_id: int) -> None:
        """Deactivate a destination"""
        command = DeactivateDestinationCommand(destination_id=destination_id)
        handler = DeactivateDestinationHandler(self._destination_repo)
        handler.handle(command)
    
    # Destination Queries
    def get_destination(self, destination_id: int) -> Optional[DestinationDTO]:
        """Get a single destination"""
        query = GetDestinationQuery(destination_id=destination_id)
        handler = GetDestinationHandler(self._destination_repo)
        return handler.handle(query)
    
    def get_all_destinations(self) -> List[DestinationDTO]:
        """Get all active destinations"""
        query = GetAllDestinationsQuery()
        handler = GetAllDestinationsHandler(self._destination_repo)
        return handler.handle(query)
    
    def get_destinations_by_region(self, region_id: int) -> List[DestinationDTO]:
        """Get destinations by region"""
        query = GetDestinationsByRegionQuery(region_id=region_id)
        handler = GetDestinationsByRegionHandler(self._destination_repo)
        return handler.handle(query)
    
    def search_destinations(self, search_query: str) -> List[DestinationDTO]:
        """Search destinations"""
        query = SearchDestinationsQuery(query=search_query)
        handler = SearchDestinationsHandler(self._destination_repo)
        return handler.handle(query)
    
    # Region Commands
    def create_region(self, command: CreateRegionCommand) -> int:
        """Create a new region"""
        handler = CreateRegionHandler(self._region_repo)
        region_id = handler.handle(command)
        return region_id.value
    
    def update_region(self, command: UpdateRegionCommand) -> None:
        """Update a region"""
        handler = UpdateRegionHandler(self._region_repo)
        handler.handle(command)
    
    # Region Queries
    def get_region(self, region_id: int) -> Optional[RegionDTO]:
        """Get a single region"""
        query = GetRegionQuery(region_id=region_id)
        handler = GetRegionHandler(self._region_repo)
        return handler.handle(query)
    
    def get_all_regions(self) -> List[RegionDTO]:
        """Get all regions"""
        query = GetAllRegionsQuery()
        handler = GetAllRegionsHandler(self._region_repo)
        return handler.handle(query)


# Singleton instance
_tourism_service = None


def get_tourism_service() -> TourismApplicationService:
    """Get the tourism application service instance"""
    global _tourism_service
    if _tourism_service is None:
        _tourism_service = TourismApplicationService()
    return _tourism_service
