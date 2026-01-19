"""
Repository interfaces for Tourism domain
These define the contract for data access without implementation details
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from shared.domain.value_objects import DestinationId, RegionId
from .destination import TouristDestination
from .region import Region


class IDestinationRepository(ABC):
    """Repository interface for TouristDestination aggregate"""
    
    @abstractmethod
    def get_by_id(self, destination_id: DestinationId) -> Optional[TouristDestination]:
        """Retrieve a destination by its ID"""
        pass
    
    @abstractmethod
    def get_all_active(self) -> List[TouristDestination]:
        """Retrieve all active destinations"""
        pass
    
    @abstractmethod
    def get_by_region(self, region_id: RegionId) -> List[TouristDestination]:
        """Retrieve all destinations in a specific region"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[TouristDestination]:
        """Search destinations by name or description"""
        pass
    
    @abstractmethod
    def save(self, destination: TouristDestination) -> None:
        """Save a destination (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, destination: TouristDestination) -> None:
        """Delete a destination"""
        pass
    
    @abstractmethod
    def exists(self, destination_id: DestinationId) -> bool:
        """Check if a destination exists"""
        pass


class IRegionRepository(ABC):
    """Repository interface for Region aggregate"""
    
    @abstractmethod
    def get_by_id(self, region_id: RegionId) -> Optional[Region]:
        """Retrieve a region by its ID"""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Region]:
        """Retrieve a region by its code"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Region]:
        """Retrieve all regions"""
        pass
    
    @abstractmethod
    def save(self, region: Region) -> None:
        """Save a region (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, region: Region) -> None:
        """Delete a region"""
        pass
    
    @abstractmethod
    def exists(self, region_id: RegionId) -> bool:
        """Check if a region exists"""
        pass
