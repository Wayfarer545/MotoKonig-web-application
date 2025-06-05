class ApplicationError(Exception):
    """Base class for application layer errors."""


class UnauthorizedError(ApplicationError):
    """Raised when authentication fails."""


class BadRequestError(ApplicationError):
    """Raised when provided data is invalid."""


class NotFoundError(ApplicationError):
    """Raised when an entity is not found."""


class TooManyRequestsError(ApplicationError):
    """Raised when too many requests are made."""


class InternalError(ApplicationError):
    """Raised for unexpected internal errors."""
