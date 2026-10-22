from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.catalog.models import Product


class ProductRepository:
    """All SQL for products lives here, and nothing else does."""
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_slug(self, slug: str) -> Product | None:
        stmt = select(Product).where(Product.slug == slug, Product.is_active.is_(True))
        return await self.session.scalar(stmt)

    async def slug_exists(self, slug: str) -> bool:
        return await self.session.scalar(select(Product.id).where(Product.slug == slug)) is not None

    async def add(self, product: Product) -> Product:
        self.session.add(product)
        return await self.save(product)

    async def save(self, product: Product) -> Product:
        await self.session.flush() # send pending SQL now, inside this transaction
        await self.session.refresh(product) # re-read DB values: ids, defaults, roundedprices
        return product