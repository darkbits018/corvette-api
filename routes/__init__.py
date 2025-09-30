# This file makes the 'routes' directory a Python package and exposes the route modules.

from . import auth
from . import users
from . import roles
from . import ips
from . import indices

# Explicitly declare the public API of the 'routes' package.
__all__ = ["auth", "users", "roles", "ips", "indices"]
