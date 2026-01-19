"""
Common value objects used across bounded contexts
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
import re
from .base import ValueObject, DomainException


class InvalidEmailError(DomainException):
    """Raised when email format is invalid"""
    pass


class InvalidPhoneNumberError(DomainException):
    """Raised when phone number format is invalid"""
    pass


class InvalidMoneyError(DomainException):
    """Raised when money value is invalid"""
    pass


class InvalidLocationError(DomainException):
    """Raised when location coordinates are invalid"""
    pass


@dataclass(frozen=True)
class Email(ValueObject):
    """Email value object"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid(self.value):
            raise InvalidEmailError(f"Invalid email format: {self.value}")
    
    @staticmethod
    def _is_valid(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __str__(self):
        return self.value


@dataclass(frozen=True)
class PhoneNumber(ValueObject):
    """Phone number value object"""
    value: str
    
    def __post_init__(self):
        if not self._is_valid(self.value):
            raise InvalidPhoneNumberError(f"Invalid phone number format: {self.value}")
    
    @staticmethod
    def _is_valid(phone: str) -> bool:
        """Validate phone number format (basic validation)"""
        if not phone or not isinstance(phone, str):
            return False
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        # Check if it contains only digits and optional + at start
        pattern = r'^\+?[0-9]{8,15}$'
        return bool(re.match(pattern, cleaned))
    
    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Money(ValueObject):
    """Money value object with currency"""
    amount: Decimal
    currency: str = "XAF"  # Central African CFA franc
    
    def __post_init__(self):
        # Validate amount
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))
        
        if self.amount < 0:
            raise InvalidMoneyError("Amount cannot be negative")
        
        # Validate currency
        if not self.currency or len(self.currency) != 3:
            raise InvalidMoneyError(f"Invalid currency code: {self.currency}")
    
    def add(self, other: 'Money') -> 'Money':
        """Add two money values"""
        if self.currency != other.currency:
            raise InvalidMoneyError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)
    
    def subtract(self, other: 'Money') -> 'Money':
        """Subtract two money values"""
        if self.currency != other.currency:
            raise InvalidMoneyError(
                f"Cannot subtract different currencies: {self.currency} and {other.currency}"
            )
        result = self.amount - other.amount
        if result < 0:
            raise InvalidMoneyError("Result cannot be negative")
        return Money(result, self.currency)
    
    def multiply(self, factor: Decimal) -> 'Money':
        """Multiply money by a factor"""
        if not isinstance(factor, Decimal):
            factor = Decimal(str(factor))
        if factor < 0:
            raise InvalidMoneyError("Factor cannot be negative")
        return Money(self.amount * factor, self.currency)
    
    def is_zero(self) -> bool:
        """Check if amount is zero"""
        return self.amount == Decimal('0')
    
    def is_greater_than(self, other: 'Money') -> bool:
        """Compare if this money is greater than another"""
        if self.currency != other.currency:
            raise InvalidMoneyError(
                f"Cannot compare different currencies: {self.currency} and {other.currency}"
            )
        return self.amount > other.amount
    
    def __str__(self):
        return f"{self.amount} {self.currency}"


@dataclass(frozen=True)
class Location(ValueObject):
    """Geographic location value object"""
    latitude: Decimal
    longitude: Decimal
    address: Optional[str] = None
    
    def __post_init__(self):
        # Convert to Decimal if needed
        if not isinstance(self.latitude, Decimal):
            object.__setattr__(self, 'latitude', Decimal(str(self.latitude)))
        if not isinstance(self.longitude, Decimal):
            object.__setattr__(self, 'longitude', Decimal(str(self.longitude)))
        
        # Validate coordinates
        if not (-90 <= self.latitude <= 90):
            raise InvalidLocationError(
                f"Latitude must be between -90 and 90, got {self.latitude}"
            )
        if not (-180 <= self.longitude <= 180):
            raise InvalidLocationError(
                f"Longitude must be between -180 and 180, got {self.longitude}"
            )
    
    def __str__(self):
        if self.address:
            return f"{self.address} ({self.latitude}, {self.longitude})"
        return f"({self.latitude}, {self.longitude})"


@dataclass(frozen=True)
class UserId(ValueObject):
    """User identifier value object"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int) or self.value <= 0:
            raise DomainException(f"Invalid user ID: {self.value}")
    
    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class DestinationId(ValueObject):
    """Destination identifier value object"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int) or self.value <= 0:
            raise DomainException(f"Invalid destination ID: {self.value}")
    
    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class ReservationId(ValueObject):
    """Reservation identifier value object"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int) or self.value <= 0:
            raise DomainException(f"Invalid reservation ID: {self.value}")
    
    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class TransactionId(ValueObject):
    """Transaction identifier value object"""
    value: str
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise DomainException(f"Invalid transaction ID: {self.value}")
    
    def __str__(self):
        return self.value


@dataclass(frozen=True)
class ReviewId(ValueObject):
    """Review identifier value object"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int) or self.value <= 0:
            raise DomainException(f"Invalid review ID: {self.value}")
    
    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class RegionId(ValueObject):
    """Region identifier value object"""
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int) or self.value <= 0:
            raise DomainException(f"Invalid region ID: {self.value}")
    
    def __str__(self):
        return str(self.value)
