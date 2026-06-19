import logging
from datetime import datetime, date, timezone
from typing import Sequence
from sqlalchemy.orm import Session
from app.data.models import Category, Product
from app.data.database import session_maker
from sqlalchemy import select, text, insert, update, func, delete
from sqlalchemy.exc import IntegrityError
import app.data.event
import pytz


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

    def get_family_category(self, category_id: int, limit: int = 10, offset: int = 0) -> Sequence[Category]:
        stmt = (select(Category).
                limit(limit).
                offset(offset).
                filter_by(parent_category_id=category_id))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_by_time_create(self, time_create: datetime, limit: int = 10, offset: int = 0) -> Sequence[Category]:
        stmt = (select(Category).limit(limit).offset(offset).filter_by(time_create=time_create))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_by_date_create(self, current_date: date, time_zone: str = 'America/New_York') -> Sequence[Category]:
        tz = pytz.timezone(time_zone)

        year, mount, day = current_date.year, current_date.month, current_date.day
        local_start = datetime(year, mount, day, 0, 0, 0)
        local_end = datetime(year, mount, day, 23, 59, 59)

        start_utc = tz.localize(local_start).astimezone(timezone.utc)
        end_utc = tz.localize(local_end).astimezone(timezone.utc)

        stmt = select(Category).filter(Category.created_at.between(start_utc, end_utc))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_by_between_date_create(self, start_date: date, end_date: date, time_zone: str = 'America/New_York') -> Sequence[Category]:
        tz = pytz.timezone(time_zone)

        s_year, s_month, s_day = start_date.year, start_date.month, start_date.day
        e_year, e_month, e_day = end_date.year, end_date.month, end_date.day

        local_start = datetime(s_year, s_month, s_day, 0, 0, 0)
        local_end = datetime(e_year, e_month, e_day, 23, 59, 59)

        start_utc = tz.localize(local_start).astimezone(timezone.utc)
        end_utc = tz.localize(local_end).astimezone(timezone.utc)

        stmt = select(Category).filter(Category.created_at.between(start_utc, end_utc))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_all(self, limit: int = 10, offset: int = 0) -> Sequence[Category]:
        stmt = (select(Category).
                limit(limit).
                offset(offset))
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def create(self, category: Category) -> Category:
        self.session.add(category)
        self.session.flush()
        self.session.commit()
        return category

    def bulk_create(self, categories: list[dict]) -> int:
        stmt = insert(Category).values(categories)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount

    def update(self, id: int, **kwargs):
        category = self.session.get(Category, id)
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            self.session.commit()
        return category

    def update_fast(self, id: int, **kwargs):
        stmt = (
            update(Category).where(Category.id == id).
            values(**kwargs)
        )
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount

    def delete(self, id: int):
        product_count = self.session.execute(
            select(func.count(Product.id)).where(Product.category_id == id)
        ).scalar()
        if product_count > 0:
            raise ValueError()
        category = self.session.get(Category, id)
        if not category:
            return False
        self.session.delete(category)
        self.session.commit()
        return True

    def delete_fast(self, id: int):
        stmt = delete(Category).where(Category.id == id)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount