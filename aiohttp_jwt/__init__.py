
__version__ = '0.0.1b'

from .exceptions import UnauthorizedError
from .middleware import JWTMiddleware
from .decorators import ensure_scopes

__all__ = (
    'JWTMiddleware',
    'ensure_scopes',
    'UnauthorizedError',
)
