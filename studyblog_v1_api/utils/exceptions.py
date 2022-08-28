"""
Module for custom exceptions.
"""

class UnauthorizedException(Exception):
    """Exception for unauthorize user access to an resource."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotAuthenticatedException(Exception):
    """Exception for unauthenticated access to an resource."""
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)