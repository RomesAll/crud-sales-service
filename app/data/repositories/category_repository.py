from typing import Sequence
from app.data.models import Category
from sqlalchemy import select
from .base import BaseRepositoryORM

class CategoryRepository(BaseRepositoryORM):
    model = Category

    def get_by_slug(self, slug: str) -> Category | None:
        return self._get_by_unique_field({'slug': slug})

    def get_by_name(self, name: str) -> Category | None:
        return self._get_by_unique_field({'name': name})

    def get_family_category(self, category_id: int, limit: int = 10, offset: int = 0) -> Sequence[Category]:
        stmt = (select(Category).
                limit(limit).
                offset(offset).
                filter_by(parent_category_id=category_id))
        categories = self.session.execute(stmt).scalars().all()
        return categories