"""
Region aggregate root - Represents a geographic region
"""
from shared.domain.base import AggregateRoot, DomainEvent, DomainException
from shared.domain.value_objects import RegionId


class InvalidRegionDataError(DomainException):
    """Raised when region data is invalid"""
    pass


# Domain Events
class RegionCreated(DomainEvent):
    """Event raised when a new region is created"""
    def __init__(self, region_id: RegionId, name: str, code: str):
        super().__init__()
        self.region_id = region_id
        self.name = name
        self.code = code


class RegionUpdated(DomainEvent):
    """Event raised when region details are updated"""
    def __init__(self, region_id: RegionId):
        super().__init__()
        self.region_id = region_id


class Region(AggregateRoot):
    """
    Region aggregate root.
    Represents a geographic region that contains tourist destinations.
    """
    
    def __init__(
        self,
        id: RegionId,
        name: str,
        code: str,
        description: str = ""
    ):
        super().__init__(id)
        self._name = name
        self._code = code.upper()
        self._description = description
        
        # Validate
        self._validate()
    
    @classmethod
    def create(
        cls,
        id: RegionId,
        name: str,
        code: str,
        description: str = ""
    ) -> 'Region':
        """Factory method to create a new region"""
        region = cls(
            id=id,
            name=name,
            code=code,
            description=description
        )
        
        # Raise domain event
        region.add_domain_event(
            RegionCreated(id, name, code)
        )
        
        return region
    
    def _validate(self):
        """Validate region invariants"""
        if not self._name or len(self._name) < 2:
            raise InvalidRegionDataError("Region name must be at least 2 characters")
        
        if not self._code or len(self._code) > 10:
            raise InvalidRegionDataError("Region code must be between 1 and 10 characters")
    
    # Properties
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def code(self) -> str:
        return self._code
    
    @property
    def description(self) -> str:
        return self._description
    
    # Business methods
    def update_details(
        self,
        name: str = None,
        description: str = None
    ):
        """Update region details (code cannot be changed)"""
        if name:
            self._name = name
        if description is not None:
            self._description = description
        
        self._validate()
        self.add_domain_event(RegionUpdated(self.id))
    
    def __repr__(self):
        return f"Region(id={self.id}, name='{self._name}', code='{self._code}')"
