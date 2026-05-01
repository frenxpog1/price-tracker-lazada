"""
Custom exception classes for the application.
Provides specific exceptions for different error scenarios.
"""


class PriceTrackerException(Exception):
    """Base exception for all application-specific errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(PriceTrackerException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTHENTICATION_ERROR")


class AuthorizationError(PriceTrackerException):
    """Raised when user lacks permission for an action."""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="AUTHORIZATION_ERROR")


class ValidationError(PriceTrackerException):
    """Raised when input validation fails."""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, code="VALIDATION_ERROR")


class NotFoundError(PriceTrackerException):
    """Raised when a requested resource is not found."""
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, code="NOT_FOUND")


class DatabaseError(PriceTrackerException):
    """Raised when database operations fail."""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, code="DATABASE_ERROR")


class ScraperError(PriceTrackerException):
    """Raised when web scraping fails."""
    def __init__(self, platform: str, message: str = "Scraping failed"):
        self.platform = platform
        super().__init__(f"{platform}: {message}", code="SCRAPER_ERROR")


class PlatformUnavailableError(ScraperError):
    """Raised when an e-commerce platform is unreachable."""
    def __init__(self, platform: str):
        super().__init__(platform, "Platform unavailable")


class EmailDeliveryError(PriceTrackerException):
    """Raised when email delivery fails."""
    def __init__(self, message: str = "Email delivery failed"):
        super().__init__(message, code="EMAIL_DELIVERY_ERROR")


class RateLimitError(PriceTrackerException):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT_ERROR")
