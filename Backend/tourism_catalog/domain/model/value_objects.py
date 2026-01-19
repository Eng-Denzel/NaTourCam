"""
Value objects specific to Tourism Catalog bounded context
"""
from dataclasses import dataclass
from decimal import Decimal
from datetime import time
from typing import Optional
from shared.domain.base import ValueObject, DomainException
from shared.domain.value_objects import Money


class InvalidVisitingHoursError(DomainException):
    """Raised when visiting hours are invalid"""
    pass


class InvalidImageError(DomainException):
    """Raised when image data is invalid"""
    pass


@dataclass(frozen=True)
class VisitingHours(ValueObject):
    """Visiting hours value object"""
    opening_time: Optional[time]
    closing_time: Optional[time]
    
    def __post_init__(self):
        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                raise InvalidVisitingHoursError(
                    f"Opening time ({self.opening_time}) must be before closing time ({self.closing_time})"
                )
    
    def is_open_24_hours(self) -> bool:
        """Check if the destination is open 24 hours"""
        return self.opening_time is None and self.closing_time is None
    
    def is_open_at(self, check_time: time) -> bool:
        """Check if the destination is open at a specific time"""
        if self.is_open_24_hours():
            return True
        if not self.opening_time or not self.closing_time:
            return False
        return self.opening_time <= check_time <= self.closing_time
    
    def __str__(self):
        if self.is_open_24_hours():
            return "Open 24 hours"
        return f"{self.opening_time} - {self.closing_time}"


@dataclass(frozen=True)
class AdmissionFee(ValueObject):
    """Admission fee value object"""
    amount: Money
    is_free: bool = False
    
    def __post_init__(self):
        if self.is_free and not self.amount.is_zero():
            raise DomainException("Free admission must have zero amount")
        if not self.is_free and self.amount.is_zero():
            object.__setattr__(self, 'is_free', True)
    
    @classmethod
    def free(cls) -> 'AdmissionFee':
        """Create a free admission fee"""
        return cls(amount=Money(Decimal('0'), 'XAF'), is_free=True)
    
    @classmethod
    def paid(cls, amount: Money) -> 'AdmissionFee':
        """Create a paid admission fee"""
        return cls(amount=amount, is_free=False)
    
    def __str__(self):
        if self.is_free:
            return "Free admission"
        return str(self.amount)


@dataclass(frozen=True)
class DestinationImage(ValueObject):
    """Destination image value object"""
    image_path: str
    caption: str = ""
    is_primary: bool = False
    
    def __post_init__(self):
        if not self.image_path:
            raise InvalidImageError("Image path cannot be empty")
    
    def __str__(self):
        return f"{self.caption or 'Image'} ({self.image_path})"


@dataclass(frozen=True)
class BilingualText(ValueObject):
    """Bilingual text value object for English and French"""
    english: str
    french: str
    
    def __post_init__(self):
        if not self.english and not self.french:
            raise DomainException("At least one language must be provided")
    
    def get_text(self, language: str) -> str:
        """Get text in specified language"""
        if language.lower() == 'fr':
            return self.french or self.english
        return self.english or self.french
    
    def __str__(self):
        return f"EN: {self.english[:50]}... | FR: {self.french[:50]}..."


@dataclass(frozen=True)
class RegionCode(ValueObject):
    """Region code value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value) > 10:
            raise DomainException(f"Invalid region code: {self.value}")
        # Ensure uppercase
        object.__setattr__(self, 'value', self.value.upper())
    
    def __str__(self):
        return self.value
