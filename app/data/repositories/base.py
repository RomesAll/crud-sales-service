import uuid
from datetime import datetime, timezone, date
from typing import Sequence
from sqlalchemy import inspect
import pytz
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models import Base
from app.data.repositories.interface import Repository


class BaseRepositoryORM(Repository):
    model: type[Base] = Base

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, limit: int = 10, offset: int = 0) -> Sequence[Base]:
        stmt = select(self.model).limit(limit).offset(offset)
        orm_objects = self.session.execute(stmt).scalars().all()
        return orm_objects

    def get_by_uuid(self, uuid: uuid.UUID):
        return self._get_by_unique_field({"uuid": uuid})

    def get_by_id(self, id: int | uuid.UUID):
        return self._get_by_unique_field({"id": id})

    def get_by_slug(self, slug: str):
        return self._get_by_unique_field({"slug": slug})

    def get_by_name(self, name: str):
        return self._get_by_unique_field({"name": name})

    def _get_by_unique_field(self, field: dict):
        stmt = select(self.model).filter_by(**field)
        result = self.session.execute(stmt).scalar()
        return result

    def get_by_date_create(
        self, current_date: date, time_zone: str = "America/New_York"
    ) -> Sequence[Base]:
        tz = pytz.timezone(time_zone)

        year, mount, day = current_date.year, current_date.month, current_date.day
        local_start = datetime(year, mount, day, 0, 0, 0)
        local_end = datetime(year, mount, day, 23, 59, 59)

        start_utc = tz.localize(local_start).astimezone(timezone.utc)
        end_utc = tz.localize(local_end).astimezone(timezone.utc)

        stmt = select(self.model).filter(
            self.model.created_at.between(start_utc, end_utc)
        )
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def get_by_between_date_create(
        self, start_date: date, end_date: date, time_zone: str = "America/New_York"
    ) -> Sequence[Base]:
        tz = pytz.timezone(time_zone)

        s_year, s_month, s_day = start_date.year, start_date.month, start_date.day
        e_year, e_month, e_day = end_date.year, end_date.month, end_date.day

        local_start = datetime(s_year, s_month, s_day, 0, 0, 0)
        local_end = datetime(e_year, e_month, e_day, 23, 59, 59)

        start_utc = tz.localize(local_start).astimezone(timezone.utc)
        end_utc = tz.localize(local_end).astimezone(timezone.utc)

        stmt = select(self.model).filter(
            self.model.created_at.between(start_utc, end_utc)
        )
        categories = self.session.execute(stmt).scalars().all()
        return categories

    def insert(self, orm_object: Base):
        self.session.add(orm_object)
        self.session.commit()
        return orm_object

    def update(self, id: int | uuid.UUID, update_data: dict):
        orm_object = self.session.get(self.model, id)
        for key, value in update_data.items():
            setattr(orm_object, key, value)
        self.session.commit()
        return orm_object

    def delete(self, id: int | uuid.UUID):
        orm_object = self.session.get(self.model, id)
        deleted_data = {column.key: getattr(orm_object, column.key)
                        for column in inspect(orm_object).columns}
        self.session.delete(orm_object)
        self.session.commit()
        return deleted_data