import uuid
from decimal import Decimal
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from app.modules.catalog.models import Category

class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    brand: str = Field(min_length=1, max_length=255)
    category: Category
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)
    warranty_months: int = Field(ge=0, default=12)
    description: str = ""
    specs: dict[str, Any] = {}

class ProductCreate(ProductBase):
    slug: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$", max_length=255)

class ProductUpdate(BaseModel):
    """Every field optional: only what the client sends is changed."""
    name: str | None = Field(default=None, min_length=2, max_length=255)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)
    warranty_months: int | None = Field(default=None, ge=0)
    description: str | None = None
    specs: dict[str, Any] | None = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    slug: str
    in_stock: bool