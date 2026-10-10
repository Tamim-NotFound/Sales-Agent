"""Import every model here so Alembic's autogenerate can see it."""

from app.modules.users.models import User # noqa: F401
from app.modules.catalog.models import Product  #noqa: F401 