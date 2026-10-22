class AppError(Exception):
    """Base class for errors the service layer raises. Never HTTP-specific."""

class NotFoundError(AppError):
    def __init__(self, resource: str, key: str) -> None:
        super().__init__(f"{resource} '{key}' not found") 

class ConflictError(AppError):
    pass