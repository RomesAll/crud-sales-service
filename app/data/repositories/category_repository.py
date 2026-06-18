from datetime import datetime
from typing import Sequence
from sqlalchemy.orm import Session
from app.data.models import Category
from sqlalchemy import select

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, category_id: int) -> Category | None:
        return self._get_by_unique_field({'id': category_id})

    def get_by_slug(self, slug: str) -> Category | None:
        return self._get_by_unique_field({'slug': slug})

    def get_by_name(self, name: str) -> Category | None:
        return self._get_by_unique_field({'name': name})

    def _get_by_unique_field(self, field: dict) -> Category | None:
        stmt = select(Category).filter_by(**field)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def get_family_category(self, category_id: int, limit: int, offset: int) -> Sequence[Category]:
        stmt = (select(Category).
                limit(limit).
                offset(offset).
                filter_by(parent_category_id=category_id))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_by_time_create(self, time_create: datetime) -> Sequence[Category]:
        stmt = select(Category).filter_by(time_create=time_create)
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_all(self, limit: int, offset: int) -> Sequence[Category]:
        stmt = (select(Category).
                limit(limit).
                offset(offset))
        categories = self.session.execute(stmt).scalars().all()
        return categories