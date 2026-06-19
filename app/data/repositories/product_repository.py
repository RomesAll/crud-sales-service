from sqlalchemy import select

from .base import BaseRepositoryORM
from ..models import Product


class ProductRepository(BaseRepositoryORM):
    model = Product

    def get_by_slug(self, slug: str) -> Product | None:
        return self._get_by_unique_field({"slug": slug})

    def get_by_name(self, name: str) -> Product | None:
        return self._get_by_unique_field({"name": name})

    def get_by_sku(self, sku: str) -> Product | None:
        return self._get_by_unique_field({"sku": sku})

    def get_active_products(self, limit: int = 10, offset: int = 0):
        stmt = select(Product).limit(limit).offset(offset).filter_by(active=True)
        products = self.session.execute(stmt).scalars().all()
        return products


