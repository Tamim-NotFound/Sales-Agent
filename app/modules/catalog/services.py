from app.core.exceptions.errors import ConflictError, NotFoundError
from app.modules.catalog.models import Product
from app.modules.catalog.repositories import ProductRepository
from app.modules.catalog.schemas import ProductCreate, ProductRead, ProductUpdate


def to_read(product: Product) -> ProductRead:
    return ProductRead.model_validate(obj=product) # reads attributes, including the in_stock property

class ProductService:
    """Business rules"""

    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    async def get_product(self, slug: str) -> ProductRead | None:
        product: Product | None = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError(resource="Product", key=slug)
        return to_read(product)

    async def create_product(self, data: ProductCreate) -> ProductRead:
        if await self.repo.slug_exists(data.slug):
            raise ConflictError(resource="Product", key=data.slug)
        product: Product | None = await self.repo.add(Product(**data.model_dump()))
        return to_read(product)

    async def update_product(self, slug: str, data: ProductUpdate) -> ProductRead:
        product: Product | None = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError(resource="Product", key=slug)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.repo.save(product)
        return to_read(product)

    async  def archive_product(self, slug: str) -> None:
        product: Product | None = await self.repo.get_by_slug(slug)
        if product is None:
            raise NotFoundError(resource="Product", key=slug)
        product.is_active = False 